# Boids mjpg streaming 

This program runs a simulation of flocking behavior targeted at a series of random points and calculates the positions of each "Boid" point using numpy ndarrays. These are then converted to jpg animation frames and streamed to the browser. Current version runs close to 20 fps with 300 flocking particles and takes about 30% of a single cpu.

## steps for running

* clone the repository
* start the python `server_code.py`
* install the svelte development server code `npm install`
* run the development environment `npm run dev`
* open a browser and navigate to localhost:5000


