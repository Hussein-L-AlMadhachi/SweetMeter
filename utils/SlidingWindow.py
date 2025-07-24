import matplotlib.pyplot as plt
from threading import Lock





class SlidingWindow_TS:
    def __init__( self , q_size ):
        self.dataset_x = [0] * q_size
        self.q_size = q_size
        self.index = q_size - 1
        
        self.mutex_lock = Lock()


    def push( self , value ):
        with self.mutex_lock:
            self.dataset_x[ self.index ] = value
            self.index += 1
            self.index %= self.q_size


    def get_nth( self , n ):
        with self.mutex_lock:
            index = ( self.index - n-1 ) % self.q_size
            return self.dataset_x[ index ]


    def plot( self ):
        def rotate_left(lst, n):
            return lst[n:] + lst[:n]
    
        with self.mutex_lock:    
            xpoints = range( 1 , len(self.dataset_x)+1 )
            ypoints = self.dataset_x

            ypoints = rotate_left( ypoints , self.index )

        plt.plot(xpoints, ypoints , 'o:y')
        plt.grid()

        plt.savefig('plot.png')
        plt.close()
        return ypoints


    def delta_n( self , n ):
        with self.mutex_lock: 
            if self.get_nth(1) == 0:
                return 0

            if self.get_nth(n) == 0:
                return self.get_nth(0) - self.get_nth(1)
            
            return (self.get_nth(0) - self.get_nth(n))/(n+1)


