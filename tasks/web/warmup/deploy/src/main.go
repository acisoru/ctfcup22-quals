package main

import (
	"context"
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

type appHandler struct {
	db *sql.DB
}

func (ah *appHandler) saveNote(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		w.WriteHeader(http.StatusMethodNotAllowed)
		fmt.Fprintln(w, "<h1>Method not allowed!</h1>")
		return
	}

	r.ParseForm()
	content := r.Form.Get("content")
	password := r.Form.Get("password")

	if content == "" || password == "" {
		w.WriteHeader(http.StatusPreconditionFailed)
		fmt.Fprintln(w, "<h1>Please specify content & password!</h1>")
		return
	}

	ctx, cancel := context.WithTimeout(context.Background(), time.Second*5)
	defer cancel()

	res, err := ah.db.ExecContext(ctx, "INSERT INTO secrets (content, password) VALUES (?, ?)", content, password)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		fmt.Fprintln(w, err.Error())
		return
	}

	secretId, err := res.LastInsertId()
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		fmt.Fprintln(w, err.Error())
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(fmt.Sprintf(`{"secretId": %d}`, secretId)))
}

func (ah *appHandler) getNote(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		w.WriteHeader(http.StatusMethodNotAllowed)
		fmt.Fprintln(w, "<h1>Method not allowed!</h1>")
		return
	}

	q := r.URL.Query()
	secretIdStr := q.Get("secretId")
	secretId, err := strconv.Atoi(secretIdStr)
	if err != nil {
		w.WriteHeader(http.StatusPreconditionFailed)
		fmt.Fprintf(w, "Invalid secretId: %v", err)
		return
	}

	ctx, cancel := context.WithTimeout(context.Background(), time.Second*3)
	defer cancel()

	rows, err := ah.db.QueryContext(ctx, fmt.Sprintf(`SELECT content FROM secrets WHERE id = %d AND password = "%s"`, secretId, q.Get("password")))
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		log.Printf("Failed to query db: %v", err)
		fmt.Fprintf(w, "Failed to get secret")
		return
	}
    defer rows.Close()

	if !rows.Next() {
		w.WriteHeader(http.StatusNotFound)
		fmt.Fprintf(w, "No secret found")
		return
	}

	var content string
	if err := rows.Scan(&content); err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		log.Printf("Failed to scan row: %v", err)
		fmt.Fprintf(w, "Failed to get secret")
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(fmt.Sprintf(`{"secretId": %d, "content": "%s"}`, secretId, content)))
}

func main() {
	pwd, err := os.ReadFile("/dbpassword")
	if err != nil {
		log.Fatal(err)
	}

	pwdStr := strings.ReplaceAll(string(pwd), "\n", "")

	db, err := sql.Open("mysql", fmt.Sprintf("root:%s@tcp(db:3306)/secrets", pwdStr))
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	app := appHandler{db: db}
	http.HandleFunc("/api/read", app.getNote)
	http.HandleFunc("/api/write", app.saveNote)
	log.Fatal(http.ListenAndServe(":5000", nil))
}

