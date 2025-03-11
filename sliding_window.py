import matplotlib
import matplotlib.pyplot as plt




mode = "prod"




class SlidingWindow:
    def __init__( self , q_size ):
        self.dataset_x = [0] * q_size
        self.q_size = q_size
        self.index = q_size - 1


    def push( self , value ):
        self.dataset_x[ self.index ] = value
        self.index += 1
        self.index %= self.q_size


    def get_nth( self , n ):
        index = ( self.index - n-1 ) % self.q_size
        return self.dataset_x[ index ]


    def plot( self ):
        def rotate_left(lst, n):
            return lst[n:] + lst[:n]
    
        xpoints = range( 1 , len(self.dataset_x)+1 )
        ypoints = self.dataset_x

        ypoints = rotate_left( ypoints , self.index )

        plt.plot(xpoints, ypoints , 'o:y')
        plt.grid()

        plt.savefig('plot.png')
        plt.close()
        return ypoints


    def delta_n( self , n ):
        if self.get_nth(1) == 0:
            return 0

        if self.get_nth(n) == 0:
            return self.get_nth(0) - self.get_nth(1)
        
        return (self.get_nth(0) - self.get_nth(n))/(n+1)


    def delta_triangle( self , n ):
        p1 = self.get_nth( n*3 )
        p2 = self.get_nth( n*2 )
        p3 = self.get_nth( n*1 )
        p4 = self.get_nth( n*0 )

        d1 = p2 - p1
        d2 = p3 - p2
        d3 = p4 - p3

        if (d1 < 0 and d2 > 0) or (d1 > 0 and d2 < 0) or (d2 < 0 and d3 > 0) or (d3 > 0 and d2 < 0):
            print( p4 , " - " , p1 )
            delta = (p4 - p1) / ((n+1)*3)
        else:
            delta = (p2 - p1) / n

        return delta





if mode == "testing":

    fake_readings = [ 
        297,309,303,305,266,255,
        224,195,175,124,130,126,
        134,143,143,139,121,119,
        122,117,114,110,107,108,
        114,120,123,125,127,130
    ]


    q = SlidingWindow( 120 )

    for sgv in fake_readings[-5:]:
        q.push( sgv )


    print( q.plot() )


    print()
    print( q.get_nth(0) )
    print( q.get_nth(1) )
    print( q.get_nth(2) )
    print( q.get_nth(3) )
    print( q.get_nth(4) )

    print( q.delta_n(4) )
    print( q.delta_triangle(4))


