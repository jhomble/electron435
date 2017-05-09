# Python Causal Parser


Stmts() : [] of Stmt
Stmt(Cond, Caus)
Cond(BoolExp)
BoolExp(Boolean, Op, Boolean)
- Op = Token of AND or OR
Boolean(e1, Op, e2) 
- Exp : one of (ALL, TYPE, LITERAL, Boolean, Var, or Args)
- Op = Token of >,<,>=,<=, or =
Caus(Act, Acts)
Act(Var, Args)
Acts() : [] of Act



The diagram provided (causaltree.jpg) breaks down the structure/code of the abstract syntax tree constructed by and traversed using the causal compiler. The root element (Stmts) is composed of a list of Stmt objects. These Stmt objects are in turn composed of a Cond (conditional) and Caus (cause) object, representing the conditions needed to be met (Cond) for a causal action (Caus) to occur.

Cond objects break down into a BoolExp (Boolean expression) composed of AND- or OR-concatenated Boolean objects, which can recursively break down into more Booleans using the >,<,>=,<=,= -concatenated generic Exp (Expression) objects. Exp objects can represent any of a series of expressions, including ALL(…), TYPE(…), LITERAL(…), Boolean, Var, or Args.

Down the other path of the tree, Caus objects break down into Act and Acts objects, where the Act object is the causal action being defined and the Acts object is a list of Act objects, representing the series of causal actions that the left-child Act causal action implies. Each Act object correspondingly decomposes into a Var object, representing the name of the causal action, and an Args object, representing the arguments of the causal action.

For the sake of space in the diagram, some of the tree’s child nodes have been replaced with a dotted line, but these nodes would normally decompose into the same structure as their siblings.
