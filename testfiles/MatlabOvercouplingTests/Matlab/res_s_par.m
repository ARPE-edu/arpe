function [S11,S12,S21,S22,f] = res_s_par(b1,b2,Q0,f0,n,rel_span)
%   res_s_par Summary: Calculates S parameters of a 2-port resonator 
%   S parameters are calculated from coupling coefficients, unloaded
%   quality factor and center frequency
%   b1= coupling parameter at port 1
%   b2= coupling parameter at port 2
%   Q0= unloaded quality factor
%   f0= center frequency
%   n= number of points in frequency sweep (>= 2)
%   rel_span= span of the frequency sweep relative to 3 dB bandwidth

%   Vector preallocations
    S11=complex(zeros(n));
    S12=complex(zeros(n));
    S21=complex(zeros(n));
    S22=complex(zeros(n));
    f=zeros(n);

%   Loaded quality factor and 3 dB bandwidth
    Ql=Q0/(1+b1+b2);
    Bw=f0/Ql;

%   Frequency span, frequency step and minimum frrewquency
    fspan=rel_span*Bw;
    fstep=fspan/(n-1);
    fmin=f0-fspan/2;

%   frequency sweep 
    for i=1:n
    f(i)=fmin+(i-1)*fstep;
    end

% S-parameters
    for i=1:n
        % delta
        d=0.5*(f(i)/f0-f0/f(i));
    
        %frequency-dependent term A
        A=(1+b1+b2)*(1+1j*2*Ql*d);
        
        % S-parameters
        S11(i)=1-2*b1/A;
        S22(i)=1-2*b2/A;
        S21(i)=-2*sqrt(b1*b2)/A;
        S12(i)=S21(i);
    end

end