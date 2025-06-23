# n-body-simulation
Simulates the gravitational interactions between point masses without collision. Uses the leapfrog method to symplectically calculate the kinematic properties of each particle at variable timesteps. Uses the kick-drift-kick form of leapfrog integration. Variable timesteps are used to deal with point masses that approach the singularity at r=0 in Newtonian gravity.
