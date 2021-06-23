Finding Lane Lines on the Road

The libraries used in this project are the following:       
    open cv,    
    numpy,  
    matplotlib,         
    moviepy 
    
The pipelining of this project are the following:       
    Selecting the region of interest (colour selection)     
    Canny edge - detection  
    hough transform 
    
Reflection
  1. Discription about my pipeline.     
    Assuming that the camera has a fixed mount on the car so the angle and shape of the road lines remain same untill and unless the lines itself starts to change shape / orientation      
    My pipeline consisted of 5 steps.   
      1. Convert the images to grayscale and then perforn canny edge detection on it.  
          as the image is greyscale the there will be a drop in the color gradient on the boundry/edges of road lines (white/yellow) which would be easily detectable and 
          hence markable    
      2. On this image we now perform region selection (or masking).  
            The entire region outside the defined polygon (here: trapezium) will be masked witha monotonic color.   
      3. On his masked edge detected image we perform hough transformation   
            After after the edge detection all pixels in our region of interest and above color threshold are lines in hough space. The interection point of these lines  
            will be a road line in normal cartesian space.  
      4. Extrapolation of lines   
           From the above algo we get lines, multiple short lines, To get a single long line we take the average of all lines we get and find the average slope and average
           y intersection. Now we have both m and c for an eqn of a sl -> y = m*x + c.
      5. Imposing of images    
          After we got the lines we draw them by modifying a null matrix of same dimensions as of origonial image and then instead of concatinating the images we perform
          weighted addition, first to get a single matrix for both the lines and then the lines with origonal image with bias 0.
        
    For videos we just apply all these steps to all the frames.


  2. Potential shortcomings with the current pipeline
      1. Can not form curved lines for eg. at a turn the algorithm could go hay wire and form an arc at best.
      2. Needs some space between it and the vehicle in front to detect the lines
      3. If a white or any bright colored object comes in the region of interest it could be inferred as road lane line and can cause havoc.


  3. Suggest possible improvements to your pipeline
      Something like object detection and radius of curvature to form a curved line would improve the algorithm a lot.
      
      
To see the examples of how does the result turn please see the photos and videos in the (folders named accordingly)
