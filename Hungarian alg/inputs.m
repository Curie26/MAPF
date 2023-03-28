%Inputs
x_init = [11 12 11 10];
y_init = [0 1 2 1];
x_targ = [1 0 1 3];
y_targ = [0 1 2 2];

%Preference
M=10
L=[M M 1 1; M M 1 1; M 1 M M ; 1 M M M ];

plot(x_init,y_init,'x','Color','b','linewidth',3)
title("Lane Preference")
%title("Mixed Platoons and All Possible Targets")
xlabel("X-Coordinate")
ylabel("Lane ID")
grid on
grid minor
hold on
set(gca,'xdir','reverse','ydir','reverse')
xlim([-1 12.5])
ylim([-0.5 2.5])
plot(x_targ,y_targ,'x','Color','r','linewidth',3)
set(gca,'YTick',[0 1 2])
set(gca,'XTick',[0 1 2 3 4 5 6 7 8 9 10 11 12])
hold off

%for i = 1:length(x_init)
    %line([x_init(1) x_targ(i)], [y_init(1) y_targ(i)],'Color','r','LineStyle',':','linewidth',2)
    %line([x_init(2) x_targ(i)], [y_init(2) y_targ(i)],'Color','g','LineStyle',':','linewidth',2)
    %line([x_init(3) x_targ(i)], [y_init(3) y_targ(i)],'Color','b','LineStyle',':','linewidth',2)
    %line([x_init(4) x_targ(i)], [y_init(4) y_targ(i)],'Color','m','LineStyle',':','linewidth',2)
%end

line([x_init(1) x_targ(3)], [y_init(1) y_targ(3)],'Color','r','LineStyle',':','linewidth',2)
line([x_init(1) x_targ(4)], [y_init(1) y_targ(4)],'Color','r','LineStyle',':','linewidth',2)
line([x_init(2) x_targ(3)], [y_init(2) y_targ(3)],'Color','g','LineStyle',':','linewidth',2)
line([x_init(2) x_targ(4)], [y_init(2) y_targ(4)],'Color','g','LineStyle',':','linewidth',2)
line([x_init(3) x_targ(2)], [y_init(3) y_targ(2)],'Color','b','LineStyle',':','linewidth',2)
line([x_init(4) x_targ(1)], [y_init(4) y_targ(1)],'Color','m','LineStyle',':','linewidth',2)


%distance calculation
cost = [];
for i=1:length(x_init)
    for j=1:length(x_targ)
        dist = sqrt((x_targ(j)-x_init(i))^2+(y_targ(j)-y_init(i))^2);
        cost(i,j) = dist;
    end
end

display(cost)

cost_pref = cost.*L

[assignment,cost]=munkres(cost_pref);

disp(assignment); 
disp(cost); 

A=zeros(size(cost_pref))

for i = 1 : length(assignment)
    A(i,assignment(i))=1;
end

display(A)

for j = 1:size(A,1)  % for each row
   for i = 1:size(A,2)  % for each collumn
      if A(i,j) ==1
          display("Vehicle is at position")
          display(x_init(i))
          display(y_init(i))
          display("Target is at position")
          display(x_targ(j))
          display(y_targ(j))
      end
   end
end






