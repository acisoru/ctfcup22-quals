#! /usr/bin/env sage

def main():
    F.<x> = GF(2)[]
    f = F.random_element(degree=48)                                                                           
    while not f.is_primitive(): 
        f = F.random_element(degree=48) 
    print(f)
    print(f.list())
    
    f_index = []
    for i,val in enumerate(f.list()[1:]):
        if val:
            f_index.append(i+1)
    f_index.reverse()
    print(f_index)
    print(f.is_irreducible())
    

if __name__ == '__main__':
    main()