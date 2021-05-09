      SUBROUTINE DFLUX(FLUX,SOL,JSTEP,JINC,TIME,NOEL,NPT,COORDS,JLTYP,
     1 TEMP,PRESS,SNAME)
C
      INCLUDE 'ABA_PARAM.INC'
C
      DIMENSION COORDS(3),FLUX(2),TIME(2)
      CHARACTER*80 SNAME


      real*8 t,pi,phi,eta,P,Q,v,S,x,y,z,x0,y0,z0,Hs,Iz,a,b,c,ff
      t=time(2)
      pi=3.1415926
      eta = 1.0
      P = 5083000.0
      v = 5
C     defining position parameters
      x=coords(1)
      y=coords(2)
      z=coords(3)
      Q = P*eta
      a = 10
      b = 2
      cf = 15
      cr = 15
      ff = 1
      fr = 1
      x0 = 0.0 + v*t
      y0 = 20 
      z0 = 20 
      heatf = 6.0*sqrt(3.0)*ff*Q/(a*b*cf*pi*sqrt(pi))
      shapef = exp(-3.0*(x-x0)**2/a**2-3.0*(y-y0)**2/b**2-3.0*(z-z0)**2/cf**2)
      heatr = 6.0*sqrt(3.0)*fr*Q/(a*b*cr*pi*sqrt(pi))
      shaper = exp(-3.0*(x-x0)**2/a**2-3.0*(y-y0)**2/b**2-3.0*(z-z0)**2/cr**2)
      IF (x >= x0) THEN
          flux(1) = heatf*shapef
      ELSE IF (x < x0) THEN
          flux(1) = heatr*shaper
      END IF
      flux(2) = 0

      RETURN
      END
