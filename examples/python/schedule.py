import opc, time
import scipy as sp
import sched
s = sched.scheduler(time.time, time.sleep)

numLEDs = 64
edge_length=10
client = opc.Client('localhost:7890')

#default value for pixels
pixels_init=[ (100,100,100) ] * numLEDs

pixels=pixels_init

#set of times at which to draw
draw_times=set()

#returns random blueish coor
def blues():
    return (100+sp.random.randint(90), 20+sp.random.randint(80), 155+sp.random.randint(100))


#draws pixels at appropriate times
def draw_pixels():
    for t in draw_times:
        s.enterabs(t,1,client.put_pixels, argument=(pixels,))

#turns on pixels starting at index p0
def set_pixels(p0,new_pixels):
#    print('time',time.time())
    pixels[p0:p0+len(new_pixels)]=new_pixels

#lights pixels starting at index p0 from time t0 to t0+dt then returns to init_pixels
def temp_pixels(p0,new_pixels,t0,dt):
    s.enterabs(t0,1,set_pixels, argument=(p0,new_pixels))
    s.enterabs(t0+dt,1,set_pixels, argument=(p0,pixels_init[p0:p0+len(new_pixels)]))
    draw_times.add(t0)
    draw_times.add(t0+dt)
    
    #why does this offest by 1?
#    s.enterabs(t0,1,set_pixels, argument=(p0,new_pixels))
#    s.enterabs(t0+dt,1,set_pixels, argument=(p0,pixels_init[p0:p0+len(new_pixels)])) #why does this offest by 1?
    #s.run()

#lights a random edge for time L for duration dt starting at time t0
def random_edge(L,t0,dt,pattern):
    for i in range(int(dt/L)):
        p0= edge_length*(sp.random.randint(numLEDs) // edge_length)
#        print(p0)
#        s.enterabs(t0+dt*i,1,set_pixels, argument=(p0,[blues()]*edge_length))
#        s.enterabs(t0+dt*i+dt,1,set_pixels, argument=(p0,pixels_init[p0:p0+edge_length])) #why does this offest by 1?
        temp_pixels(p0,pattern,t0+i*L,L)


#draw random edges with given pattern for t seconds
def random_edges(t,pattern):
    random_edge(.1,time.time()+1,t,pattern)
    draw_pixels()
    s.run()
    draw_times.clear()



x=[]
def print_time(t0): 
    x.append(time.time())
    print("time: ",time.time()-t0)

def print_times(t0):
    s.enterabs(time.time()+1, 1, print_time, argument=(t0,))
    s.enterabs(time.time()+2, 1, print_time, argument=(t0,))

    
def print_some_times():
    t0=time.time()
    print(time.time()-t0)
    s.enter(1,1,print_times,argument=(t0,))
    s.run()
    print(time.time()-t0)