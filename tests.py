##########################
# TESTS DE ELDA
##########################


##########################
# 2 ) fibonacci
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
# 3 ) bubble sort 
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


program void globalFunc;

var int : i, aux, a[8], length = 8, d;
var bool : isValid = True, swapped = False;

void start{

    a[0] = 60; a[1] = 10; a[2] = 4; a[3] = 9;
    a[4] = 3; a[5] = 1; a[6] = 2; a[7] = 6;

    i = 0;
    while( i < length ){
        print(a[i]);
        i = i + 1;
    }

    while( d < length - 1){
        swapped = False;
        i = 0;
        while( i < length - 1){
            if(a[i] > a[i+1]){
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

    print(0);

    i = 0;
    while( i < length ){
        print(a[i]);
        i = i + 1;
    }
}


##########################
# 4 ) find en un arreglo
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
# 5 ) factorial iterativo 
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
# 6 ) multiplicación de matrices
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


##########################
# 7 ) lasso
##########################

program void globalFunc;

var int : matrix[10][2];

void start{
    
    matrix[0][0] = 11;
    matrix[0][1] = 3;
    matrix[1][0] = 2;
    matrix[1][1] = 2;
    matrix[2][0] = 37;
    matrix[2][1] = 3;
    matrix[3][0] = 4;
    matrix[3][1] = 444;
    matrix[4][0] = 5;
    matrix[4][1] = 5;
    matrix[5][0] = 99;
    matrix[5][1] = 6;
    matrix[6][0] = 7;
    matrix[6][1] = 75;
    matrix[7][0] = 8;
    matrix[7][1] = 18;
    matrix[8][0] = 9;
    matrix[8][1] = 9;
    matrix[9][0] = 134;
    matrix[9][1] = 10;

    lasso( matrix );

}


##########################
# 8 ) ridge
##########################

program void globalFunc;

var int : matrix[10][2];

void start{
    
    matrix[0][0] = 11;
    matrix[0][1] = 3;
    matrix[1][0] = 2;
    matrix[1][1] = 2;
    matrix[2][0] = 37;
    matrix[2][1] = 3;
    matrix[3][0] = 4;
    matrix[3][1] = 444;
    matrix[4][0] = 5;
    matrix[4][1] = 5;
    matrix[5][0] = 99;
    matrix[5][1] = 6;
    matrix[6][0] = 7;
    matrix[6][1] = 75;
    matrix[7][0] = 8;
    matrix[7][1] = 18;
    matrix[8][0] = 9;
    matrix[8][1] = 9;
    matrix[9][0] = 134;
    matrix[9][1] = 10;

    ridge( matrix, 5 );

}


##########################
# 8 ) linear regression
##########################

program void globalFunc;

var int : matrix[10][2];

void start{
    
    matrix[0][0] = 11;
    matrix[0][1] = 3;
    matrix[1][0] = 2;
    matrix[1][1] = 2;
    matrix[2][0] = 37;
    matrix[2][1] = 3;
    matrix[3][0] = 4;
    matrix[3][1] = 444;
    matrix[4][0] = 5;
    matrix[4][1] = 5;
    matrix[5][0] = 99;
    matrix[5][1] = 6;
    matrix[6][0] = 7;
    matrix[6][1] = 75;
    matrix[7][0] = 8;
    matrix[7][1] = 18;
    matrix[8][0] = 9;
    matrix[8][1] = 9;
    matrix[9][0] = 134;
    matrix[9][1] = 10;

    linear_regression( matrix, 2 );

}


##########################
# 9 ) MINI BATCH
##########################

program void globalFunc;

var int : matrix[10][2];

void start{
    
    matrix[0][0] = 11;
    matrix[0][1] = 3;
    matrix[1][0] = 2;
    matrix[1][1] = 2;
    matrix[2][0] = 37;
    matrix[2][1] = 3;
    matrix[3][0] = 4;
    matrix[3][1] = 444;
    matrix[4][0] = 5;
    matrix[4][1] = 5;
    matrix[5][0] = 99;
    matrix[5][1] = 6;
    matrix[6][0] = 7;
    matrix[6][1] = 75;
    matrix[7][0] = 8;
    matrix[7][1] = 18;
    matrix[8][0] = 9;
    matrix[8][1] = 9;
    matrix[9][0] = 134;
    matrix[9][1] = 10;

    mini_batch( matrix, 2 );

}


##########################
# 10 ) T_SERIES NO JALA EN EXTRA FUNCTIONS CODE
##########################

program void globalFunc;

var int : matrix[10][2], list[7];

void start{
    
    matrix[0][0] = 11;
    matrix[0][1] = 3;
    matrix[1][0] = 2;
    matrix[1][1] = 2;
    matrix[2][0] = 37;
    matrix[2][1] = 3;
    matrix[3][0] = 4;
    matrix[3][1] = 444;
    matrix[4][0] = 5;
    matrix[4][1] = 5;
    matrix[5][0] = 99;
    matrix[5][1] = 6;
    matrix[6][0] = 7;
    matrix[6][1] = 75;
    matrix[7][0] = 8;
    matrix[7][1] = 18;
    matrix[8][0] = 9;
    matrix[8][1] = 9;
    matrix[9][0] = 134;
    matrix[9][1] = 10;

    list[0] = 1;
    list[1] = 2;
    list[2] = 3;
    list[3] = 4;
    list[4] = 5;
    list[5] = 6;
    list[6] = 7;

    t_series( matrix, list, 4 );

}


##########################
# 11 ) mean_abs_err
##########################

program void globalFunc;

var int : matrix[10][2], matrixTwo[10][2];

void start{
    
    matrix[0][0] = 11;
    matrix[0][1] = 3;
    matrix[1][0] = 2;
    matrix[1][1] = 2;
    matrix[2][0] = 37;
    matrix[2][1] = 3;
    matrix[3][0] = 4;
    matrix[3][1] = 444;
    matrix[4][0] = 5;
    matrix[4][1] = 5;
    matrix[5][0] = 99;
    matrix[5][1] = 6;
    matrix[6][0] = 7;
    matrix[6][1] = 75;
    matrix[7][0] = 8;
    matrix[7][1] = 18;
    matrix[8][0] = 9;
    matrix[8][1] = 9;
    matrix[9][0] = 134;
    matrix[9][1] = 10;

    matrixTwo[0][0] = 11;
    matrixTwo[0][1] = 3;
    matrixTwo[1][0] = 2;
    matrixTwo[1][1] = 2;
    matrixTwo[2][0] = 37;
    matrixTwo[2][1] = 3;
    matrixTwo[3][0] = 4;
    matrixTwo[3][1] = 444;
    matrixTwo[4][0] = 5;
    matrixTwo[4][1] = 5;
    matrixTwo[5][0] = 99;
    matrixTwo[5][1] = 6;
    matrixTwo[6][0] = 7;
    matrixTwo[6][1] = 75;
    matrixTwo[7][0] = 8;
    matrixTwo[7][1] = 18;
    matrixTwo[8][0] = 9;
    matrixTwo[8][1] = 9;
    matrixTwo[9][0] = 134;
    matrixTwo[9][1] = 10;


    mean_abs_err( matrix, matrixTwo );

}


##########################
# 12 ) mean, mode, median, freq, variance, stddev, kurt
##########################

program void globalFunc;

var int : array[10];

void start{

    array[0] = 1;
    array[1] = 2;
    array[2] = 3;
    array[3] = 4;
    array[4] = 5;
    array[5] = 6;
    array[6] = 7;
    array[7] = 8;
    array[8] = 9;
    array[9] = 1;

    kurt( array );

}















##########################
# TEST MISC
##########################

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
# funciones y valores de retorno
##########################

program void globalFunc;

var int : i,j;

func void uno( int a ){
    
    i = a * 2;
    if( i < a + 4 ){
        uno(a + 1);
    }
    print(i);
} 

func void dos( int b ){
    b = b * i + j;
    return( b * 2 )
}

void start{
    i = 2;
    j = i * 2 - 1;
    uno(j);
    print( i + dos( i + j) );

}


##########################
# funciones y valores de retorno
##########################

program void globalFunc;

var int : i,j;

func int uno(){
    i = 2;
    return 2;
} 

void start{
    j = uno();
    print(2);
    return 2;

}


##########################
# 1 ) expresiones
##########################

program void globalFunc;

var int : A, B, C, D,E,F,K,H,J,G,L;

void start{
    
    A = B + C * ( D - E / F ) * H;
    B = E - F;

    while(A * B - C >= D * E / ( G + H) ){
        H = J * K + B;
        if( B < H ){
            B = H + J;
            while( B > A + C ){
                print( A + B * C, D - E );
                B = B - J;
            }
        }else{
            do{
                A = A + B;
                print( B - D );
            }while( A - D < C + B )
        }
    }

    F = A + B;
}






