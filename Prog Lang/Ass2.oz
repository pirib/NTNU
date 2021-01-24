functor
import
    System
define

    % <================================================== Task 1 
    % Copied from the assignment 1
    \insert list.oz 
    
    % <================================================== Task 2
    % a

    fun {Lex Input} 
        {String.tokens Input & }
    end
 
    % b - terribly unelegant, but very readable
    fun {Tokenize Lexemes}

        % Make sure there is something in the Lexemes
        if {Length Lexemes} > 0 then
            
            % See what it is, and create a record of the accoding type
            if {String.isInt Lexemes.1}  then
                number( { String.toInt Lexemes.1} ) | {Tokenize Lexemes.2}
            elseif Lexemes.1 == "+" then
                operator(type:plus) | {Tokenize Lexemes.2}
            elseif Lexemes.1 == "-" then
                operator(type:minus)| {Tokenize Lexemes.2}
            elseif Lexemes.1 == "*" then
                operator(type:multiply)| {Tokenize Lexemes.2}
            elseif Lexemes.1 == "/" then
                operator(type:divide) | {Tokenize Lexemes.2}
            elseif Lexemes.1 == "p" then
                command(name: print) | {Tokenize Lexemes.2}
            elseif Lexemes.1 == "d" then
                command(name: duplicate) | {Tokenize Lexemes.2}
            elseif Lexemes.1 == "i" then
                command(name: negate) | {Tokenize Lexemes.2}        % I used the name negate, for the invert command
            elseif Lexemes.1 == "^" then
                command(name: inverse) | {Tokenize Lexemes.2}    
            else 
                % Just so i know if there is an error in the input
                % Will ignore these in the next tasks
                error(type:unknown) | {Tokenize Lexemes.2}  
            end

        else
            nil
        end
    end

    % C 
    proc {Interpret Tokens} Iterate DoMath in 

        % Does all the fun math stuff
        fun { DoMath Op Stack} 
            if Op == plus then        
                Stack.2.1 + Stack.1
            elseif Op == minus then
                Stack.2.1 - Stack.1     % I honestly dont know if it shold be this way or another
            elseif Op == multiply then
                Stack.2.1 * Stack.1
            elseif Op == divide then    
                {IntToFloat  Stack.2.1} / {IntToFloat  Stack.1}     % Same here
            else
                {System.showInfo "did not recognize the operand"}
            end
        end         

        % Iteratres through the stack
        proc {Iterate Stack Tokens} TS in   %TS stands for tempStack 

            % If a number, push onto the stack
            case Tokens.1 of number(N) then
                TS = N | Stack
            % If the type is unknown, ignore it 
            [] operator(type:O) then
                if O == unknown then
                    % skipping unindentified input
                    {System.showInfo "Found an unknown value, skipping"}
                    TS = Stack
                    skip

                % Yes, it is an abomination of ORs. Yes, I feel bad for doing it this way 
                % Checking if it is an operand, running the DoMath that will return the result, and popping it to the Stack minus the elements used in the calculation
                elseif { Or {Or O == plus O == minus} {Or O == divide O == multiply}} then
                    TS = {DoMath O Stack} | {Drop Stack 2} 
                end

            % If it is of type command, emmm do it? I think it is pretty straightforward
            [] command(name: C) then
                if C == print then
                    {System.show Stack}
                    TS = Stack
                elseif C == duplicate then
                    TS = Stack.1 | Stack
                elseif C == negate then
                    TS = ~ Stack.1 | {Drop Stack 1}
                elseif C == inverse then
                    TS =  {IntToFloat 1}/{IntToFloat Stack.1} | {Drop Stack 1}
                end                
            end
            
            % If the Token list still has other elements other than nil, recurse call the Iterate procedure, with the remainder of the Token list
            % Else, just print out the TS
            if Tokens.2 \= nil then
                {Iterate TS Tokens.2}
            else
                {System.show TS}        % This is the return value 
            end

        end
        
        {Iterate nil Tokens}

    end
    
    % Voila
    {Interpret {Tokenize {Lex "1 2 3 +"}}} 

    {Interpret {Tokenize {Lex "1 2 3 p +"}}}

    {Interpret {Tokenize {Lex "1 2 3 + d"}}}


    % Task 3 - works like a charm, but in my case output is ASCII, so it is difficult to say for sure (used conversions online, looked all correct to me)
    % High-level description is in the comments just follow the yellow brick road ! (and no, i am not sorry for that reference)

    fun {Infix Tokens} InfixInternal in

        fun {InfixInternal Tokens ExpressionStack} TES in
            % Grabbing the tokens
            % If it is a number, push into the stack
            case Tokens.1 of number(N) then
                TES = N | ExpressionStack
            % If it is an operator, pop the two values on top, concatenate them with each other and the sign
            [] operator(type:O) then
                if O == plus then
                    TES = "("#ExpressionStack.1#" + "#ExpressionStack.2.1#")" | { Drop ExpressionStack 2}
                elseif O == minus then
                    TES = "("#ExpressionStack.1#"-"#ExpressionStack.2.1#")" | { Drop ExpressionStack 2}
                elseif O == multiply then
                    TES = "("#ExpressionStack.1#"*"#ExpressionStack.2.1#")" | { Drop ExpressionStack 2}
                elseif O == divide then
                    TES = "("#ExpressionStack.1#"/"#ExpressionStack.2.1#")" | { Drop ExpressionStack 2}
                end
            % If it is the command, do the same (Except for the inverse, but that is self explanatory)
            [] command(name:C) then
                if C == negate then
                    TES = "("#ExpressionStack.1#"i )" | { Drop ExpressionStack 2}
                elseif C == inverse then
                  TES = "("#ExpressionStack.1#"^"#ExpressionStack.2.1#")" | { Drop ExpressionStack 1}
                end
            end

            % If the Token list still has other elements other than nil, recurse call the InfixInternal, with the remainder of the Token list
            % Else, just return the TES - Temporary Expression Stack
            if Tokens.2 \= nil then
                {InfixInternal Tokens.2 TES} 
            else
                TES
            end
        end

        {InfixInternal Tokens nil}

    end

    {System.show {Infix {Tokenize {Lex "3 10 + 5 1 1 i ^"}}}}

/*  TASK 4

a.  Formally describe the regular grammar of the lexemes in task 2.

    Using the notation from CTMCP 2.1
    <operator> ::= + | - | * | /
    <command>  ::= p | d | i | ^
    <number>   ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9      
    or, assuming it would support floats 
    <number>   ::= [0...9]* | [0...9]*.[0...9]


b. Describe the grammar of the infix notation in task 3 using (E)BNF. Beware of operator precedence. Is the grammar ambiguous? Explain why it is or is not ambiguous?

I will be reusing <operator> <command> and <number> from task 4a.

<expression> ::= (<expression> | <number>) <operator> ( <expression> | <number> ) ) | ( ( <expression> | <number> ) <command>) 

I think this grammar is unambigious, given that there is a pretty hefty restriction on what can constitute an expression - there is no room for ambiguity here, so to speak.
The first "half" indicates that the expression constitutes a combo of a pair of two numbers and/or expressions, while the second adds another rule to accomodate the i and ^.


c. What is the difference between a context-sensitive and a context-free grammar?

    The grammars described in task a and b are context-free - the expansion of any non-terminal (operator, command, number) will always be the same.
    Context-sensitive grammar adds conditionalities to a context-free one. 
    Thus they become context sensitive, meaning that in addition to rules defined by context-free grammar we also need into account the context in which a particular instance of the language is implemented.


d. You may have gotten float-int errors in task 2. If you haven’t, try running1+1.0. Why does this happen?Why is this a useful error?

    Int and Float are two different types - e.g. their representation is different and thus they might have different operations that one is permitted to use overe them.
    This way we can diferentiate between the two when either is undersired.

*/


end