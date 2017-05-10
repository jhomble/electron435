# Python Causal Compiler

## Lexer

The lexer converts the raw input text into a token stream fed to the parser. Look in Lexer.py for more info. 

## Parser

The parser converts the token stream from the lexer into an Abstract Syntax Tree (AST) which is described below:

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

## Compiler

## Example

```
RULES {
	move-to(obj, dest, dx, dy, dz, da) := grasp(obj), release(obj, dest, dx, dy, dz, da);
	if (TYPE(obj)=block || TYPE(obj)=specialCupcake): 
		stack(dest, dx, dy, dz, da, obj) := move-to(obj, dest, dx, dy, dz, da)
}
```

The code segment above describes two causal relationships, one direct and one conditional: 
- The first statement can be taken to mean that if the program observes a grasp of "obj" and then a release of "obj" at a given location "dest," the inferred intention behind this action is a move-to of the "obj" to "dest."
- The second statement means that if the program observes a move-to of "obj" to "dest," it can be inferred that the intention was to create a stack with "obj" at "dest." However, this causal relationship is only valid if the type of "obj" is block or "specialCupcake."
