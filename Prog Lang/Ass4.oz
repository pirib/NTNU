functor import System OS define 

% For testing

% Task 1
fun {GenerateOdd S E} 
    if {Int.isOdd S} andthen S =< E then
        S | {GenerateOdd S+2 E} 
    elseif {Int.isEven S} andthen S + 1 =< E then
        S + 1 | {GenerateOdd S+3 E}
    else
        nil
    end
end

{System.showInfo "Task 1 ===================================="}
{System.show{GenerateOdd ~3 10}}    % The Assignment text has an error, it is misssing a 7
{System.show{GenerateOdd 3 3}}
{System.show{GenerateOdd 2 2}}


% Task 2

% Another product function
fun {Product List} 

    case List 
        of H | T then H * {Product T}
        [] nil then 1
    end

end

{System.showInfo "Task 2 ===================================="}
{System.show{Product [1 2 3 4]}}

% Task 3

% Stream Product 
fun {StreamProduct} S P in 

    thread S = {GenerateOdd 0 1000} end
    thread P = {Product S} end

    % Waiting for threads to finish to return the Product
    {Wait S} {Wait P}
    P
end

{System.showInfo "Task 3 ===================================="}
{System.show {StreamProduct}}
{System.showInfo "The first three digits are 100"}

/* 
To make sense of the threads, I introduced a Delay in the odd number generator and Browsed (Using the Emacs environment, that is) the accumulated product value within every given stage of the Product function.
Since the two threads above are executing in parallel, the Product function is executing concurrently with the odd number generator.
It gets suspended every time the Tail is unbounded, but gets back on track once that value becomes available. If one removes the threads alltogether Product function must wait for the GenerateOdd to finish first.
Hence, threads increase the speed of execution, assuming one uses a multi-core processor. 
*/

% Task 4


fun lazy{GenerateOddLazy S E} 
    if {Int.isOdd S} andthen S =< E then
        S | {GenerateOddLazy S+2 E} 
    elseif {Int.isEven S} andthen S + 1 =< E then
        S + 1 | {GenerateOddLazy S+3 E}
    else
        nil
    end
end

local X in

    {System.showInfo "Task 4 ===================================="}
    % Bind X to the return value of GenerateOddLazy
    X = {GenerateOddLazy 0 10}
    % returns _<optimized>
    {System.show X}

    % Force the lazy function do to the computaiton
    {Wait X}
    % Voila
    {System.show X}

end

/* 
Keyword lazy indicates that the execution of the function is halted until it is needed.
As an example, GenerateOddLazy is called, but its value is not needed (neither for the System.show command nor for the unification).
When Wait command is used, on the other hand, it sends a message to the lazy function and forces it to do the calculations.

Currently, StreamProduct works as a simple consumer - producer with GenerateOdd being the producer. 
It generates odd numbers continiously, until the limit is reached. The consumer picks up the values as fast as it can and produces the product of those. 

Feeding the GenerateOddLazy into the StreamProduct will change the pace - the producer will only produce at the request of the consumer.
This ensures that the odd numbers are generated based on the demand, and the consumer will never get overwhelmed by the producer.
Having said that, the throughput is going to decrease quite a bit, since there is an overhead between each demand and production - e.g. a trigger is required for every production.
*/

% Task 5
% The Random function from the assignment
fun {RandomInt Min Max} X = {OS.rand} MinOS MaxOS in 
    {OS.randLimits ?MinOS ?MaxOS}
    Min + X*(Max - Min) div (MaxOS - MinOS)
end

% a
{System.showInfo "Task 5a ===================================="}
fun lazy {HammerFactory}
    % Takes a whole second to produce a hammer
    %{Delay 1000}

    % 1 in 10 chance of producing a defect hammer
    if {RandomInt 0 9} == 1 then
        defect | {HammerFactory}
    else    
        working | {HammerFactory}
    end

end

% Testing the solution
local HammerTime B in
    {System.showInfo "Starting the HammerFactory"}

    HammerTime = {HammerFactory}
    
    % Forcing the lazy function to be evaluated 4 times
    B = HammerTime.2.2.2.1
    
    {System.show HammerTime}
end

%b
{System.showInfo "Task 5b ===================================="}
fun {HammerConsumer HammerStream N}
    
    if N \= 0 then
        case HammerStream 
        of H | T then 
            if H == working then
                1 + {HammerConsumer T N-1}
            else
                {HammerConsumer T N-1}
            end
        end
    else 
        0
    end
end

% Testing the solution
local HammerTime Consumer in
    
    HammerTime = {HammerFactory}
    Consumer = {HammerConsumer HammerTime 10}
    
    {System.showInfo "Out of 10 produced hammers working number is: "}
    {System.show Consumer}

end


%c
{System.showInfo "Task 5c ===================================="}

% The handsome BoundedBuffer
% Takes in the stream HammerStream, our hammer factory
% N is the maximum capacity of the buffer
% The buffer is akin to a FIFO stack with the max num elements equal N
fun {BoundedBuffer HammerStream N} 
    
    % End, in a nutshell looks N elements into the Hammer Factory production
    End = thread {List.drop HammerStream N} end
    
    % The loop fucntion gets into the Stream and get the N elements ready.
    % This is where the N elements are "stored" (not really, but you catch my drift)
    % It will stop producing a stream once the end of the list reached which is N elements long
    fun lazy {Loop HammerStream End}
        case HammerStream of H|T then
            H | {Loop T thread End.2 end}
        end
    end

in
    % well, the actual call is happening here.
    {Loop HammerStream End}
end

/*
    A bit difficult to see over here, but the calculation times are around 10 and 16 sec as the assignment suggests
    The buffer one gets 6 elements within the 6 seconds delay that it has. 
    So it has 6 hammers in the store, meaning it is 6 seconds ahead of the non-buffer produciton factory.
*/

local HammerStream Buffer Consumer in
    
    HammerStream = {HammerFactory}
    Buffer = {BoundedBuffer HammerStream 6}
    
    {Delay 6000}
    
    Consumer = {HammerConsumer Buffer 10}
    {System.show Consumer}

end

local HammerStream Consumer in
   
    HammerStream = {HammerFactory}
   
    {Delay 6000}
   
    Consumer = {HammerConsumer HammerStream 10}
    {System.show Consumer}

end

end