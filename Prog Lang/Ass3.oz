functor import Application System define


proc {QuadraticEquation A B C ?RealSol ?X1 ?X2} D in
    % Here is the D = b^2 - 4ac
    D = B*B - ( 4.0 * A * C )

    if D < 0.0 then
        RealSol = false
    else
        % In case where D is 0 then X1 = X2
        RealSol = true
        X1 = ( ~B + {Float.sqrt D } ) / ( 2.0 * A )
        X2 = ( ~B - {Float.sqrt D } ) / ( 2.0 * A )
    end

end

% <=================================================== Task 1
local 
    RealSol X1 X2
in
    {QuadraticEquation 2.0 1.0 ~1.0 RealSol X1 X2}
    
    {System.showInfo "Real solution exists: "}
    {System.show RealSol}
    
    {System.showInfo "X1 is "}
    {System.show X1}

    {System.showInfo "X2 is "}
    {System.show X1}
end

local 
    RealSol X1 X2
in
    {QuadraticEquation 2.0 1.0 2.0 RealSol X1 X2}
    
    {System.showInfo "Real solution exists: "}
    {System.show RealSol}

    % Real solution does not exist, so the following two fill be undefined    
    {System.showInfo "X1 is "}
    {System.show X1}

    {System.showInfo "X2 is "}
    {System.show X2}
end


% b - Why are procedural abstractions useful? Give at least two reasons.
/* 
    Procedural abstractions are one of the most powerful tools available to the programmer - its utility value is of course the main reason why they are so useful. 
    They provide a way of reusing the code and a nice encapsulation technique helping to structure it, e.g. convert any statement into a procedure value.
*/

% c - What is the difference between a procedure and a function?
/*  
    Procedures do not return a value, while functions do.
*/

% <=================================================== Task 2

% My old implementation of Length List
fun {Length List}
   if List == nil then
      0
   else
      1 + {Length List.2}
   end
end

% Indeed very similar!
fun {Sum List}
   if List == nil then
      0
   else
      List.1 + {Sum List.2}
   end
end

local L = [1 2 3] in
    {System.show {Sum L}}
end


% <=================================================== Task 3

% a and b
/*  The right fold funtion takes: 
1. A list List as a parameter, 
2. Op is the operation that will be performed 
3. U is the "helper" value
*/
fun {RightFold List Op U}
    % If we have recursively reached the end of the list return the helper function (0 in both cases)
    % Would be 1, if for example, are multiplication is performed
    if List == nil then
        U
    % Else, we perform the operation between the first element and the return value of the RightFold
    % This is the part that allows us to recursively use operation Op on all elements in the list, right to left
    else
        {Op List.1 {RightFold List.2 Op U} }
    end
end

% c 
% I called them Sum2 and Length2 so I can keep the original Sum and Length
fun {Sum2 List} Op in
    
    % The function that is passed as an argument
    % More readabale this way
    Op = fun {$ X Y} X+Y end    

    % Calling right folding with the freshly defined sum function
    {RightFold List Op 0 }

end

fun {Length2 List} Op in

    % A bit of unused X here, but but
    Op = fun {$ X Y} 1 + Y end

    {RightFold List Op 0 }

end

% Outputing stuff
local L = [1 2 3] in
    {System.showInfo "The length of L is"}
    {System.show {Length2 L}}
    {System.showInfo "The sum of all elements of L is"}
    {System.show {Sum2 L}} 
end

% d - For the Sum and Lenght operations, would left fold (a lef-associative fold) and right fold give different results? What about subtractions?
/*
    For both Sum and Length it would not matter since the operation performed is arithmetic plus, e.g. they both are commutative
    Substraction is another story though (since it is not commutative) - [1 2 3] with Right fold would yield 3 - 2 - 1 = 0, while leftfold would give 1 - 2 - 3 = -4
*/ 

% e - What is a good value for U when using RightFold to implement the product of list elements?
/*
    I accidentaly answered this question on line 98 - we should use 1, since U is the return value is used for the operation.
    Supplying it with 0 would mean the answer will always be 0.
*/ 

% <=================================================== Task 4

% I guess this is what is expected to be provided?
% Returns a function F that takes in one argument X, which solves quadratic equation
fun {Quadratic A B C} F in
    F = fun {$ X} 
            A * X * X + B * X + C 
        end

    % Returning F
    F
end

{System.show {{Quadratic 3 2 1} 2}} 

% <=================================================== Task 5

% a 

% Instead of commenting this out I will provide explanations in task 5b. This one took me like 3 hours but I am so damn proud of it.
fun {LazyNumberGenerator StartValue} F in

    F = fun {$}
            { LazyNumberGenerator StartValue + 1 }
        end

    StartValue | F
end

{System.showInfo "The Lazy Number Generator"} 

{System.show {LazyNumberGenerator 0}.1 }

{System.show {{LazyNumberGenerator 0}.2}.1 }

{System.show {{{{{{LazyNumberGenerator 0}.2}.2}.2}.2}.2}.1  }


% b - Give a high-level desciption of your solution and point out any limitations you find relevant
/* 
    The above function returns an embedded structure where the tail is function handle.
    Whenever the shorthand .1 is used, the head is accessed, being a number, 
    while whenever .2 is used the function handler of F is returned, which runs the LazyNumberGenerator recursevily in a delayed fashion,
    thus expanding the list.

    In terms of limitations - this might be not the fastest way of generating a list on demand - a function that spits out a list of given size would do the job much better.
*/


% <=================================================== Task 6

% a - Is your Sumfunction from Task 2 tail recursive?  If yes, explain why.  If not, implement a tail recursiveversion and explain how your changes made it so.
/* 
    In my case it is not, since the first iteration needs to wait for the last one to finalize the answer. A simple patch up though will fix things up.
*/

fun {SumTail List Sum}
   if List == nil then
      Sum
   else
      {SumTail List.2 Sum + List.1}
   end
end

local L = [1 2 3] in
    {System.show {SumTail L 0}}
end

/* 
    Now, instead of waiting for the first iterative step, every value is carried onto the next recursion step, meaning the entire data can be saved onto the same stack (hence the optimisation discussed in the next question).
*/


% b - What is the benefit of tail recursion in Oz?
/*
    Tail recursion is optimized in Oz and gains performance speed in comparison to normal recursion. (http://mozart2.org/mozart-v1/doc-1.4.0/tutorial/node6.html)
*/

% c - Do all programming languages that allow recursion benefit from tail recursion? Why/why not?
/*
    A very general question, so i think the general answer is in order - it would depend on the language. 
    Some, like Oz provide explicit optimisations for it, as the manual states. Others, certain strict functional languages do not do so. (http://mozart2.org/mozart-v1/doc-1.4.0/tutorial/node6.html)
*/




{Application.exit 0}

end