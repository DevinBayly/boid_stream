#%%
import time
from itertools import product
import cv2
import numpy as np

from http.server import SimpleHTTPRequestHandler
import socketserver
#%%
#%%
import time
from itertools import product
import cv2
import numpy as np

from http.server import SimpleHTTPRequestHandler
import socketserver
#%%

class Boids:
    dim = 800
    frame = np.ones((dim,dim,3)).astype("uint8")*255
    nbhds = np.array([list(product(np.arange(-1,1), np.arange(-1,1)))])
    positions = None
    def init(self):
        print( "boid init")
        self.positions = np.random.random((300,2))*self.dim 
        # self.positions = np.array([[0,0],[0,0],[200,200]]).astype("float")
        self.seek_pos = np.random.randint(0,self.dim,(1,2))
        self.velocity = np.random.random((300,2))*3 - 1.5
        # self.velocity = np.array([[5,5],[0,0],[0,0]])
    def update(self):
        self.frame[:,:] = 255
        # self.velocity = np.zeros((3,2),dtype = "int")
        ## non collision
        separations = self.positions[None,:,:] - self.positions[:,None,:]

        square_displacement = separations*separations
        square_displacement

        square_dist = square_displacement.sum(axis=2)

        alert_distance = 50
        close_birds = square_dist< alert_distance
        close_birds

        separations_if_close = np.copy(separations)
        far_away_mask = np.logical_not(close_birds)
        ## makee far away birds separations zero 
        far_away_mask

        separations_if_close[:,:][far_away_mask] = 0

        # must make sum to a 100,2 array
        #fly away from the points where distance was too small
        ## the 0 axis is avoid
        avoid_dir = separations_if_close.sum(0) 


        # corners
        middle = np.mean(self.positions)
        direction_to_mid = self.positions - middle
        # zero the infs
        # direction_to_mid[np.isinf(direction_to_mid)] = 0
        center_attract_force = .07
        self.velocity = np.around(self.velocity - direction_to_mid*center_attract_force).astype("int")
        if np.mean(np.absolute(self.seek_pos - self.positions)) <100:
           self.seek_pos = np.random.randint(0,self.dim,(1,2))
           print(self.seek_pos)
        direction_to_seek = self.positions - self.seek_pos
        seek_strength = .05
        self.velocity = np.around(self.velocity - direction_to_seek*seek_strength).astype("int")

        ## make velocity send bird away from near ones
        self.velocity = (self.velocity + avoid_dir*.18)
        ## attempt to match nearby bird speed
        vseps = self.velocity[None,:,:] - self.velocity[:,None,:] 
        ## calculate the squares
        formation_distance = 600
        very_far = square_dist > formation_distance
        vdif_if_close = np.copy(vseps)
        vdif_if_close[:,:][very_far] = 0
        self.velocity += np.mean(vdif_if_close,1)
        


        

        self.velocity[np.absolute(self.velocity) > 100]  = 2
        self.positions += self.velocity
        frame_pos = np.copy(self.positions).astype("int")
        s = (self.nbhds + frame_pos[:,None]).reshape(-1,2).clip(0,self.dim-1)
        self.frame[s[:,0],s[:,1]] = 0
        return self.frame

class ImageGenerator:
    def init(self):
        self.b = Boids()
        self.b.init()
    def generate(self):
        while True:
            frame = self.b.update()
            (flag,jpg) = cv2.imencode(".jpg",frame)
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(jpg) + b'\r\n')



class MyClass(SimpleHTTPRequestHandler):
    IG = None
    def path_branch(self):
        print(self.path)
        if "image" in self.path:
            self.send_response(200)
            self.send_header("Content-Type","multipart/x-mixed-replace; boundary=frame")
            self.end_headers()
            self.IG.init()
            # here's where the cv stuff would happen
            while True:
                self.wfile.write(next(self.IG.generate()))
                time.sleep(.05)
            return True
        return False
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin","*")
        SimpleHTTPRequestHandler.end_headers(self)
    def do_GET(self):
        ## split the results
        if not self.path_branch():
            SimpleHTTPRequestHandler.do_GET(self)
MyClass.IG = ImageGenerator()
with socketserver.TCPServer(("",8001),MyClass) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("shutting down")
        httpd.shutdown()
#
##%%
#pic = (np.random.random((50,50,3))*255).astype("uint8")
#(flag,jpg) = cv2.imencode(".jpg",pic)
#jpg
#
## %%
#bytearray(jpg)
#
## %%
#my_ig = ImageGenerator()
#next(my_ig.generate())
#
## %%
#boid_count=10#
#limits=np.array([2000,2000])
#
#
#positions = np.random.rand(2,boid_count)*limits[:,np.newaxis]
#positions
#
#
#def new_flock(count,lower_limits,upper_limits):
#    width = upper_limits-lower_limits
#    return (lower_limits[:,np.newaxis] + np.random.rand(2,count)*width[:,np.newaxis])
#
#
#positions = new_flock(boid_count,np.array([100,100]),np.array([4000,4000]))
#
#
#velocities = new_flock(boid_count,np.array([0,-20]),np.array([10,20]))
#
#
#
#
#boid_count = 100
#positions = new_flock(boid_count,np.array([100,100]),np.array([4000,4000]))
#velocities = new_flock(boid_count,np.array([0,-20]),np.array([10,20]))
#
#def update_boids(positions, velocities):
#    positions += velocities
#
#
#def animate(frame):
#    update_boids(positions, velocities)
#    scatter.set_offsets(positions.transpose())
#
#def convertJPG(positions):
#    frame = np.zeros((4000,4000,3))
#
#
#
#
#
### I don't think this is a very good approach, doing all the numpy manipulations to changes the frame into a animation scene will take to long
##%%
#
#nbhds = np.array([list(product(np.arange(-6,6), np.arange(-6,6)))])
##%%
#size = 1000
#dim =4000
#start = time.time()
#positions = np.random.randint(0,dim,(size,2))
#frame = np.ones((dim,dim,3)).astype("uint8")*255
##%%
##%%
#start = time.time()
#time.time() - start
##%%
#Image.fromarray(frame)
##%%
#mark_inds.shape
##%%
##%%
#rands = (np.random.rand((10))*20).astype("uint8")
#rands
## want to create [-2,-1,0,1,2] for each
#num = 2
#operation = np.linspace()
##%%
#points
##%%
#
#from itertools import product
#nbhds = np.array([list(product(np.arange(-2,3), np.arange(-2,3)))])
##%%
#s = (nbhds + points[:,None] )
#s = s.reshape(-1,2).clip(0,size-1)
#np.where(s == 100)
##%%
#frame[s[:,0],s[:,1]] = 0
##%%
#Image.fromarray(frame)
##%%
#.reshape(-1,2).clip(0,size-1)
#frame[s[:,0], s[:,1]] = 0
#
## %%
#nbhds
#
## %%
#points[None,...]
#
## %%
#
#%%
# def test() :
#     positions = np.random.randint(0,400,(100,2))
#     velocity = np.random.randint(0,2,(100,2))
#     middle = np.mean(positions)
#     print(middle)
#     direction_to_mid = positions - middle[:,np.newaxis]
#     print(direction_to_mid)

# test()
# # %%
