package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"errors"
	"fmt"
	"math/rand"
	"net/http"
	"os"
	"strconv"
	"time"

	"github.com/gorilla/mux"
	log "github.com/sirupsen/logrus"
)

type User struct {
	ID          int    `json:"id"`
	Login       string `json:"login"`
	Password    string `json:"password"`
	Coins       int    `json:"coins"`
	CurrentTask string `json:"task"`
	TaskResult  int
}

var currentMaxID = 0

var Flag = os.Getenv("GPB_MATH_PONG_FLAG")

var FlagPrice, _ = strconv.Atoi(os.Getenv("GPB_MATH_PONG_FLAG_PRICE"))

var UsersDB = []User{}

var CookiesDB = map[string]int{}

func InitUser(login string, password string) (User, error) {
	for _, v := range UsersDB {
		if login == v.Login {
			return User{}, fmt.Errorf("user already exists")
		}
	}
	user := User{ID: currentMaxID, Login: login, Password: password, Coins: 1, CurrentTask: "2+2", TaskResult: 4}
	log.Info(fmt.Sprintf("Creating new user: %v", user))
	UsersDB = append(UsersDB, user)
	currentMaxID++
	return user, nil
}

func GetUserByCookie(w http.ResponseWriter, r *http.Request) (User, error) {
	cookie, err := r.Cookie("auth")
	if err != nil {
		switch {
		case errors.Is(err, http.ErrNoCookie):
			log.Warn(fmt.Sprintf("%v tried to use %v without signin", r.RemoteAddr, r.RequestURI))
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusBadRequest)
			result, _ := json.Marshal(map[string]string{"err": "signin and recieve cookie to work with that endpoint"})
			w.Write(result)
			return User{}, fmt.Errorf("cookie not found")
		default:
			log.Warn(err)
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusInternalServerError)
			result, _ := json.Marshal(map[string]string{"err": "internal server error"})
			w.Write(result)
			return User{}, fmt.Errorf("server error")
		}
	}
	if userID, ok := CookiesDB[cookie.Value]; ok {
		for _, user := range UsersDB {
			if user.ID == userID {
				return user, nil
			}
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusInternalServerError)
		result, _ := json.Marshal(map[string]string{"err": "cannot find user with this cookie"})
		w.Write(result)
		return User{}, fmt.Errorf("user with requested credentials doesn't exists")
	} else {
		log.Warn(fmt.Sprintf("%v tried to use %v with bad cookie", r.RemoteAddr, r.RequestURI))
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusBadRequest)
		result, _ := json.Marshal(map[string]string{"err": "bad cookie, signin and receive correct one"})
		w.Write(result)
	}
	return User{}, fmt.Errorf("signin before using this endpoint")
}

func renderJson(w http.ResponseWriter, data []byte) {
	w.Header().Set("Content-Type", "application/json")
	w.Write(data)
}

func generateTask() (string, int) {
	s1 := rand.NewSource(time.Now().UnixNano())
	r1 := rand.New(s1)
	var task string
	var taskResult int
	a := r1.Intn(100) + 1
	b := r1.Intn(100) + 1
	task = strconv.Itoa(a) + "+" + strconv.Itoa(b)
	taskResult += a + b
	for i := 0; i < (r1.Intn(20) + 5); i++ {
		randomInt := r1.Intn(100) + 1
		op := r1.Intn(2)
		if op == 0 {
			task = task + "+" + strconv.Itoa(randomInt)
			taskResult += randomInt
		} else {
			task = task + "-" + strconv.Itoa(randomInt)
			taskResult -= randomInt
		}
	}
	return task, taskResult
}

func apiHandler(w http.ResponseWriter, r *http.Request) {
	var result []byte
	result, _ = json.Marshal(map[string]map[string]string{
		"GET /": {
			"auth":   "none",
			"desc":   "return api description",
			"params": "none",
		},
		"GET /api/": {
			"auth":   "none",
			"desc":   "same as /",
			"params": "none",
		},
		"GET /api/user": {
			"auth":   "required",
			"desc":   "return a user info",
			"params": "none",
		},
		"POST /api/signup": {
			"auth":   "none",
			"desc":   "signup method. needed to create your account. needed login and password",
			"params": "{'login': string, password': string}",
		},
		"POST /api/signin": {
			"auth":   "none",
			"desc":   "signin method. needed to create your account. needed login and password. sets a cookie to work with api",
			"params": "{'login': string, password': string}",
		},
		"GET /api/shop": {
			"auth":   "required",
			"desc":   "return a price for a flag",
			"params": "none",
		},
		"POST /api/shop": {
			"auth":   "required",
			"desc":   "try to buy a flag",
			"params": "none",
		},
		"GET /api/task": {
			"auth":   "required",
			"desc":   "return a task to mine coins",
			"params": "none",
		},
		"POST /api/task": {
			"auth":   "required",
			"desc":   "if answer in POST body correct, give 1 coin and return a new task. In request, send only integer number",
			"params": "int",
		},
	})
	renderJson(w, result)
}

func signinHandler(w http.ResponseWriter, r *http.Request) {
	var result []byte
	var tmp struct {
		Login    string `json:"login"`
		Password string `json:"password"`
	}
	err := json.NewDecoder(r.Body).Decode(&tmp)
	if err != nil {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusBadRequest)
		result, _ := json.Marshal(map[string]string{"err": "cannot decode json in your request"})
		w.Write(result)
		return
	}
	login := tmp.Login
	password := tmp.Password
	for _, v := range UsersDB {
		if v.Login == login && v.Password == password {
			log.Info(fmt.Sprintf("%v successfuly logged in as user %v", r.RemoteAddr, v.Login))
			h := sha256.New()
			h.Write([]byte(login + password))
			bs := base64.StdEncoding.EncodeToString(h.Sum(nil))
			//TODO delete expired cookies goroutine
			cookie := http.Cookie{
				Name:     "auth",
				Value:    bs,
				Path:     "/",
				MaxAge:   172800,
				HttpOnly: true,
				Secure:   true,
				SameSite: http.SameSiteLaxMode,
			}
			CookiesDB[bs] = v.ID
			http.SetCookie(w, &cookie)
			result, _ = json.Marshal(map[string]string{"result": "login successful"})
			renderJson(w, result)
			return
		}
	}
	result, _ = json.Marshal(map[string]string{"result": "login unsuccessful"})
	renderJson(w, result)
}

func signupHandler(w http.ResponseWriter, r *http.Request) {
	var result []byte
	var tmp struct {
		Login    string `json:"login"`
		Password string `json:"password"`
	}
	err := json.NewDecoder(r.Body).Decode(&tmp)
	if err != nil {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusBadRequest)
		result, _ := json.Marshal(map[string]string{"err": "cannot decode json in your request"})
		w.Write(result)
		return
	}
	login := tmp.Login
	password := tmp.Password
	_, err = InitUser(login, password)
	if err != nil {
		log.Info(fmt.Sprintf("%v tried to create user with already existing credentials", r.RemoteAddr))
		result, _ = json.Marshal(map[string]string{"err": "login already used"})
		renderJson(w, result)
		return
	}
	result, _ = json.Marshal(map[string]string{"result": "registration succesful"})
	renderJson(w, result)
}

func userHandler(w http.ResponseWriter, r *http.Request) {
	var result []byte
	user, err := GetUserByCookie(w, r)
	if err != nil {
		return
	}
	log.Info(fmt.Sprintf("%v checked his user info", user.Login))
	result, _ = json.Marshal(map[string]string{"result": fmt.Sprintf("user %v currently have %v coins", user.Login, user.Coins)})
	renderJson(w, result)
}

func shopHandler(w http.ResponseWriter, r *http.Request) {
	var result []byte
	user, err := GetUserByCookie(w, r)
	if err != nil {
		return
	}
	log.Info(fmt.Sprintf("%v checked shop", user.Login))
	result, _ = json.Marshal(map[string]string{"result": fmt.Sprintf("flag price is %v coins", FlagPrice)})
	renderJson(w, result)
}

func shopPostHandler(w http.ResponseWriter, r *http.Request) {
	var result []byte
	user, err := GetUserByCookie(w, r)
	if err != nil {
		return
	}
	log.Info(fmt.Sprintf("%v tried to buy flag", user.Login))
	if user.Coins >= FlagPrice {
		log.Info(fmt.Sprintf("%v succesfuly buyed flag", user.Login))
		user.Coins -= FlagPrice
		result, _ = json.Marshal(map[string]string{"result": fmt.Sprintf("succesfully buyed flag"), "flag": Flag})
		renderJson(w, result)
	} else {
		log.Info(fmt.Sprintf("%v haven't enough coins to buy a flag", user.Login))
		result, _ = json.Marshal(map[string]string{"err": "not enough coins"})
		renderJson(w, result)
	}
}

func taskHandler(w http.ResponseWriter, r *http.Request) {
	var result []byte
	user, err := GetUserByCookie(w, r)
	if err != nil {
		return
	}
	log.Info(fmt.Sprintf("%v checked his current task", user.Login))
	result, _ = json.Marshal(map[string]string{"result": user.CurrentTask})
	renderJson(w, result)
}

func taskPostHandler(w http.ResponseWriter, r *http.Request) {
	var result []byte
	user, err := GetUserByCookie(w, r)
	if err != nil {
		return
	}
	buf := new(bytes.Buffer)
	buf.ReadFrom(r.Body)
	var answer int
	err = json.Unmarshal(buf.Bytes(), &answer)
	if err != nil {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusBadRequest)
		result, _ := json.Marshal(map[string]string{"err": "when answer on a task, send only int number in post body"})
		w.Write(result)
		return
	}
	log.Info(fmt.Sprintf("%v tried to solve task", user.Login))
	if answer == user.TaskResult {
		log.Info(fmt.Sprintf("%v correctly solves task, his current balance is %v coins", user.Login, user.Coins+1))
		for i, v := range UsersDB {
			if v.ID == user.ID {
				UsersDB[i].Coins += 1
				task, taskResult := generateTask()
				UsersDB[i].CurrentTask = task
				UsersDB[i].TaskResult = taskResult
				result, _ = json.Marshal(map[string]string{"result": "answer correct, 1 coin awarded", "task": task})
			}
		}
	} else {
		result, _ = json.Marshal(map[string]string{"err": "answer incorrect"})
	}
	renderJson(w, result)
}

func RecoveryMiddleware(h http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		defer func() {
			err := recover()
			if err != nil {
				log.Warn(err)
				result, _ := json.Marshal(map[string]string{
					"err": "There was an internal server error",
				})
				w.Header().Set("Content-Type", "application/json")
				w.WriteHeader(http.StatusInternalServerError)
				w.Write(result)
			}
		}()
		h.ServeHTTP(w, r)
	})
}

func LogMiddleware(h http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		log.Info(fmt.Sprintf("%v connect to %v", r.RemoteAddr, r.RequestURI))
		h.ServeHTTP(w, r)
	})
}

func main() {
	log.SetFormatter(&log.TextFormatter{
		DisableColors: false,
		FullTimestamp: true,
	})
	log.SetLevel(log.TraceLevel)
	log.SetOutput(os.Stdout)
	log.Info("Starting HTTP server...")
	router := mux.NewRouter()
	router.HandleFunc("/", apiHandler).Methods("GET")
	router.HandleFunc("/api/", apiHandler).Methods("GET")
	router.HandleFunc("/api/signin", signinHandler).Methods("POST")
	router.HandleFunc("/api/signup", signupHandler).Methods("POST")
	router.HandleFunc("/api/user", userHandler).Methods("GET")
	router.HandleFunc("/api/shop", shopHandler).Methods("GET")
	router.HandleFunc("/api/shop", shopPostHandler).Methods("POST")
	router.HandleFunc("/api/task", taskHandler).Methods("GET")
	router.HandleFunc("/api/task", taskPostHandler).Methods("POST")
	router.Use(LogMiddleware)
	router.Use(RecoveryMiddleware)
	http.Handle("/", router)
	log.Info(fmt.Sprintf("Server started on %v", os.Getenv("GPB_MATH_PONG_PORT")))
	http.ListenAndServe(os.Getenv("GPB_MATH_PONG_PORT"), nil)
}
