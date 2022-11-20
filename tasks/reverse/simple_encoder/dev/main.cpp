#include <iostream>
#include <dlfcn.h>
#include <stdint.h>
#include <memory>
#include <stdexcept>
#include <vector> //for debug
#include <iomanip>
#include <fstream>

#define STACKSIZE 4096
class Stack
{
private:
    uint32_t head;
    std::unique_ptr<int32_t[]> stack;
public:
    Stack() { this->head = 0; this->stack = std::unique_ptr<int32_t[]>(new int[STACKSIZE]{0}); }
    void push(int value)
    {
        if (this->head == STACKSIZE) { return; }
        this->stack[this->head] = value;
        this->head++;
    }
    int pop()
    {
        if (this->head == 0) { return -1; }
        this->head--;
        uint32_t res = this->stack[this->head];
        this->stack[this->head] = 0;
        return res;
    }
    bool isEmpty()
    {
        return this->head == 0 ? true : false;  
    }
    //destructors for pussies
};

#define MEMORYSIZE 4096
class BinWriter
{
private:
    uint32_t cursor;                  //bit cursor
    std::unique_ptr<uint8_t[]> memory;

    void writeBit(uint8_t bit)
    {
        //std::cout << (int)(char)bit << " " << this->getMemoryIndex() << " " << this->getLocalCursor() << std::endl;
        bit = bit & 1;
        this->memory[this->getMemoryIndex()] |= (bit << (sizeof(uint8_t)*8-1-this->getLocalCursor()));
        this->cursor++;
    }
public:
    BinWriter() {this->cursor=0;this->memory=std::unique_ptr<uint8_t[]>(new uint8_t[MEMORYSIZE]{0});}
    uint32_t getMemoryIndex() { return  this->cursor / (sizeof(uint8_t)*8); }
    uint32_t getLocalCursor() { return  this->cursor % (sizeof(uint8_t)*8); }
    void writeData(uint32_t value, uint8_t bit_size)
    {
        Stack backstack;
        for (int bound=0; bound < bit_size; bound++)
        {
            uint8_t c_bit = value & 0x01;
            value >>= 1;
            backstack.push(c_bit);
        }

        while (!backstack.isEmpty())
        {
            this->writeBit(backstack.pop());
        }
    }
    uint8_t* getMemoryOwnership()
    {
        return memory.get();
    }
    void printMemory(uint32_t start, uint32_t end) // debug
    {
        for (int i = start; i < end; i++){
            std::cout << std::setfill('0') <<std::setw(2) <<std::hex << (int)(this->memory[i]) << " ";
        }
        std::cout << std::endl;
    }
};

struct GolombeCode
{
     uint32_t value;
     uint32_t bit_size;
};

struct GolombeCode GolombeEncode(uint32_t value)
{
    uint32_t new_value = 0;
    new_value = value + 1;
    uint8_t prefix_len =  (32 - __builtin_clz(new_value)) - 1;
    uint8_t value_len  = 32 - __builtin_clz(new_value);
    struct GolombeCode res = {.value=new_value, .bit_size=(prefix_len+value_len)};
    return res;
}


void fileWrite(const std::string& filepath, BinWriter& writer)
{
    std::ofstream inp(filepath, std::ios::out | std::ios::binary);
    inp.write((const char *)writer.getMemoryOwnership(), writer.getMemoryIndex()+1);
    inp.close();
}

std::vector<int> fileRead(const std::string& filepath)
{
    std::ifstream inp(filepath, std::ios::in | std::ios::binary);
    std::vector<int> res;
    if (inp.is_open())
    {
        while (!inp.eof())
        {
            res.push_back((int)inp.get());
        }
        inp.close();
    }
    res.pop_back();
    return res;
}

int main(int argc, char** argv)
{      
    BinWriter memory;
    if (argc != 3)
    {
        std::cout << "Use " << argv[0] << " <input> <output>" << std::endl;
        return -1;
    }

    std::vector<int> data = fileRead(argv[1]);
    for(int& i : data)
    {
        auto res = GolombeEncode(i);
        memory.writeData(res.value, res.bit_size);
    }
    fileWrite(argv[2], memory);
    std::cout << "[+] Done" <<std::endl;
    return 0;
}
