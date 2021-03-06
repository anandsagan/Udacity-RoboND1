import numpy as np
import random



# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Example:
    # Check if we have vision data to make decisions with
    #if Rover.stuckcount >0 and Rover.stuckcount<10:
          #  if Rover.stuckcount<5:
         #       Rover.throttle = -1.0
         #       Rover.steer = 0
          #      Rover.stuckcount = Rover.stuckcount+1
          #      if Rover.stuckcount ==2:
          #          Rover.stuckcount = 0
#    elif Rover.stuckcount == 0: 
    if Rover.nav_angles is not None:
            # Check for Rover.mode status


            #if Rover.counter==75:
           #     Rover.counter=0
        if Rover.mode == 'forward': 
                #rovpos = np.zeros([75,2])
               # rovpos[:,:]=randint(0,100),randint(0,100)
               # posO = np.empty([1,2])
              #  posO= np.int(Rover.pos[0]), np.int(Rover.pos[1])
               ## rovpos[Rover.counter,:]=posO
               # Rover.counter = Rover.counter+1 
                # Check the extent of navigable terrain
                if len(Rover.nav_angles) >= Rover.stop_forward:  
                    # If mode is forward, navigable terrain looks good 
                    # and velocity is below max, then throttle 
                    if Rover.vel < Rover.max_vel:
                        # Set throttle value to throttle setting
                        
                            Rover.throttle = Rover.throttle_set
                    else: # Else coast
                        Rover.throttle = 0
                    Rover.brake = 0
                    # Set steering to average angle clipped to the range +/- 15
                    if len(Rover.rock_angle) > 2:
                        Rover.steer = np.clip(np.mean(Rover.rock_angle * 180/np.pi), -15, 15)
                        if Rover.mean_rockdists < 30:
                            Rover.throttle = 0
                            Rover.brake = ((Rover.vel)**2)/40
                        elif Rover.mean_rockdists < 2:
                            Rover.mode = 'stop'                        
                    else:
                        Rover.steer = np.clip(np.median(Rover.nav_angles *Rover.nav_dists* 180/np.pi), -15, 15)    
                        #if np.all(rovpos[0,:]==rovpos[74,:]):
                          #  Rover.mode = 'stuck'
                    # If there's a lack of navigable terrain pixels then go to 'stop' mode
                elif len(Rover.nav_angles) < Rover.stop_forward:
                        # Set mode to "stop" and hit the brakes!
                        Rover.throttle = 0
                        # Set brake to stored brake value
                        Rover.brake = Rover.brake_set
                        Rover.steer = 0
                        Rover.mode = 'stop'


            # If we're already in "stop" mode then make different decisions
     #       elif Rover.mode == 'stuck':
        #        Rover.stuckcount = Rover.stuckcount+1
        elif Rover.mode == 'stop':
                # If we're in stop mode but still moving keep braking
                if Rover.vel > 0.2:
                    Rover.throttle = 0
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                # If we're not moving (vel < 0.2) then do something else
                elif Rover.vel <= 0.2:
                    # Now we're stopped and we have vision data to see if there's a path forward
                    if len(Rover.nav_angles) < Rover.go_forward:
                        Rover.throttle = 0
                        # Release the brake to allow turning
                        Rover.brake = 0
                            # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turnin
                        if len(Rover.rock_angle)>2:
                            if Rover.mean_rockdists>1:
                                Rover.throttle = 0.2
                                Rover.steer = np.clip(np.median(Rover.rock_angle * 180/np.pi), -15, 15)
                            else:
                                Rover.steer = np.clip(np.median(Rover.rock_angle * 180/np.pi), -15, 15)

                        else:
                            
                            Rover.steer = 45 # Could be more clever here about which way to turn
                    # If we're stopped but see sufficient navigable terrain in front then go!
                    if len(Rover.nav_angles) >= Rover.go_forward:
                        # Set throttle back to stored value
                        Rover.throttle = Rover.throttle_set
                        # Release the brake
                        Rover.brake = 0
                        # Set steer to mean angle
                        Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -45, 45)
                        Rover.mode = 'forward'
        # Just to make the rover do something 
        # even if no modifications have been made to the code
        else:
            Rover.throttle = Rover.throttle_set
            Rover.steer = 0
            Rover.brake = 0

        # If in a state where want to pickup a rock send pickup command
        if Rover.near_sample:
            if Rover.vel == 0 and not Rover.picking_up:
                Rover.send_pickup = True
            else:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.mode = 'stop'

    

    return Rover