

##########################
# 1 ) ciclos
##########################

program void globalFunc;

var int : i, aux, a[8], length = 8;

void start{

    a[0] = 60; a[1] = 10; a[2] = 4; a[3] = 9;
    a[4] = 3; a[5] = 1; a[6] = 2; a[7] = 6;

    while( i < length - 1 ){

        if(a[i] > a[i+1]){
            print(0);
        }
        i = i + 1;
    }
}



##########################
# 2 ) fibonacci que jala
##########################

program void globalFunc;

var int : 
    n, first, second, next, c; 

void start{
    second = 1;
    n = 40;
    while( c <= n ){

        if( c <= 1){
            next = c;
        }
        else{
            next = first + second;
            first = second;
            second = next;
        }
        print(next);
        c = c + 1;
    }
}



##########################
# 3 ) bubble sort como debe ser que no jala
##########################
program void globalFunc;

var int : i, aux, a[8], length = 7;
var bool : isValid = True, swapped = False;

void start{

    a[0] = 60; a[1] = 10; a[2] = 4; a[3] = 9;
    a[4] = 3; a[5] = 1; a[6] = 2; a[7] = 6;


    while( isValid == True ){
        swapped = False;
        i = 0;
        while( i < length ){
            if(a[i] > a[i+1]){
                print(a[i]);
                print(a[i+1]);
                aux = a[i + 1];
                a[i+1] = a[ i ];
                a[i] = aux;
                swapped = True;
            }
            if( swapped == False ){
                isValid = False;
            }   
            i = i + 1;
        }  
    }   
}


##########################
# 4 ) bubble sort que jala pero es naco
##########################

program void globalFunc;

var int : i, aux, a[8], length = 8, d;
var bool : isValid = True, swapped = False;

void start{

    a[0] = 60; a[1] = 10; a[2] = 4; a[3] = 9;
    a[4] = 3; a[5] = 1; a[6] = 2; a[7] = 6;

    while( d < length - 1){
        swapped = False;
        i = 0;
        while( i < length - 1){
            if(a[i] > a[i+1]){
                print(a[i]);
                print(a[i+1]);
                aux = a[i + 1];
                a[i+1] = a[ i ];
                a[i] = aux;
                swapped = True;
            }
            if( swapped == False ){
                isValid = False;
            }   
            i = i + 1;
        } 
        d = d + 1; 
    }  
}


##########################
# 5 ) find en un arreglo que si jala
##########################

program void globalFunc;

var int : i, aux, a[8], length = 8, numberToFind = 10;

void start{

    a[0] = 60; a[1] = 10; a[2] = 4; a[3] = 9;
    a[4] = 3; a[5] = 1; a[6] = 2; a[7] = 6;


    while( i < length - 1){
        if( a[ i ] == numberToFind ){
            print( True );
            return True;
        }
        i = i + 1;
    }

    print( False );
    return False;
    
}


##########################
# 6 ) factorial iterativo que si jala
##########################

program void globalFunc;

var int : n = 10, fact=1;

void start{
    
    while( n > 0 ){
        fact = fact * n;
        n = n -1;
    }

    print( fact );  
}



##########################
# 7 ) multiplicación de matrices que si jala
##########################

program void globalFunc;

var int : i, j, k, a[2][2], b[2][2], c[2][2], aDim = 2, bDim = 2, cDim = 2, aux1, aux2, aux3;

void start{
    
    a[0][0] = 1; 
    a[0][1] = 2; 
    a[1][0] = 3; 
    a[1][1] = 4; 

    b[0][0] = 1; 
    b[0][1] = 2; 
    b[1][0] = 3; 
    b[1][1] = 4; 

    while( i < aDim ){
        while( j < bDim ){
            while( k < cDim  ){
                aux1 = c[i][j];
                aux2 = a[i][k];
                aux3 = b[k][j];
                c[i][j] = aux1 + aux2 * aux3;
                k = k +1;
            }
            k = 0;
            j = j + 1;
        }
        j = 0;
        i = i + 1;
    }

    i = 0;
    j = 0;

    while( i < aDim ){
        while( j < bDim ){
            print( c[i][j]);
            j = j + 1;
        }
        j = 0;
        i = i + 1;
    }

}










