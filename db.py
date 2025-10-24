"""
#The mock table
#Each child (the key) is a row, and the table has 2 columns (the "sub-keys" - name and year of birth of the child)
Some DB rules:
1. Column name cannot be same in value as the data
"""
import networkx as nx
import pylab
import matplotlib

my_graph = nx.DiGraph()
my_graph.add_node("Start")
myfamily = {
  "child1" : {
    "name" : "A",
    "year" : 2000
  },
  "child2" : {
    "name" : "B",
    "year" : 2005
  },
  "child3" : {
    "name" : "C",
    "year" : 2025
  },
  "child4" : {
    "name" : "D",
    "year" : 2025
  }
}

def print_my_graph():
    print("Printing my_graph")
    nx.draw(my_graph, with_labels=True, font_weight='bold')
    pylab.show()

def select_statement(columns, propositions):
    """
    #The place where we hope to add the defensive code
    #In an actual DB implementation like mysql, you may find that some AST will give us this, and that would be where we place the checks
    Some checks:
    1. LHS of proposition should be a table name (to prevent blind sqli that uses AND 1=1, AND 1=2, for example)
    2. In case of tautology attacks in general, also check that LHS is not equal to RHS? If LHS=RHS, then game lost/return 0. We work here with the principle that 
    column names cannot be the same as the values held inside. So, we check just the values for now. In reality, if this principle, isn't
    applicable, i.e., if the column name can be the same as the value, then checking for types can be another way. That is, the type of LHS
    cannot be the same as RHS. In our example, we can consider the types to be the variable names.
    Simply put, the above can be said to be:
    type(LHS)ANDvalue(LHS)!=type(RHS)ANDvalue(RHS)
    3. We assume select * ... will be the query form
    """
    if propositions == "Nil":
        print(myfamily)
        print(myfamily.keys())
    else:
        #find the key(s) relating to the values, and add to the dicts, and print them all. Check here that the types are different.
        #check for only ANDs and ORs for now - tokenize by these, and then by "=". In real DBs, a lexer-parser would do all this.
        and_connector = "AND"
        or_connector = "OR"
        and_exists = False
        or_exists = False
        #first check AND, then OR, if both exist, then tokenize by AND first, then OR - the usual order of precedence
        if and_connector in propositions:
            and_exists = True
        if or_connector in propositions:
            or_exists = True
            
        #The below settings allow coarse (stronger) to fine grain (weaker) protection against SQLi
        with_sqli_tautology_prevention = True#where the use case is to accept propositions, but not accept tautologies in proposition. While weaker, this is to acknowledge that we may not be able to reject every logic keyword related to a proposition (AND, OR etc.)
        with_sqli_proposition_prevention = False#where the use case is to prevent propositions altogether in user input - a stronger protection
        
        #the game can be where this check is/is not good to add
        if and_exists or or_exists:
            #tokenize by and and or, after checking if either or both exist, and then do similar to below. Maybe a function for the below?
            #We call that function as the security function? The game is then to call that function or not.
            #PoC for the OR condition for starters. AND only, and AND and OR both TBC.
            if with_sqli_proposition_prevention:#This would be the highest level of protection. It would be a technically dangerous business use case which would allow logic propositions such as AND or OR in the user input.
                print("Invoking the protection 'with_sqli_proposition_prevention'")
                print("Possible SQLi thwarted, as the user sent a proposition, please check this proposition",propositions)#return 0 for the game?
            elif with_sqli_tautology_prevention and not with_sqli_proposition_prevention:
                print("SQL Injection check to be added here")
                if or_exists and not and_exists:
                    print("Will tokenise for the OR keyword")
                    prop_list=propositions.split("OR")
                    print("prop_list is",prop_list)
                    for prop in prop_list:
                        prop=prop.strip()
                        select_retrieval(prop)
            else:
                print(myfamily)#terribly dangerous, merely for demonstrating today's weaknesses of not using the necessary preventions.
                #select_retrieval(propositions)
        else:
            #selecting for a single prop
            select_retrieval(propositions)

#The expected method that can help prevent tautology-based SQLi
def select_retrieval(prop):
    print("Will try to retrieve",prop)
    tokens=prop.split("=")#to hold the propositional variables
    print(tokens)
    desired_column=tokens[0]#The column the user desires to query (The LHS)
    my_graph.add_node(desired_column)
    my_graph.add_weighted_edges_from([("Start",desired_column,2.0)])
    desired_value=tokens[1]#The value the user desires to check in that column (The RHS)
    my_graph.add_node(desired_value)
    my_graph.add_weighted_edges_from([(desired_column,desired_value,2.0)])
    if desired_column != desired_value:#Assuming that DBMSs shouldn't allow values to be the same as the column name as Codd's rules, ACID, normalization rules etc. If the assumption is wrong, then we can try to check for the types. But either way, the original assumption is to guard against abuse cases such as a tautology based sqli, and doesn't cover use cases themselves.
        for row in myfamily.keys():
            row_contents = myfamily[row]
            for column in row_contents.keys():
                if desired_column in column:#This could be an sql injection prevention check too, we check the proposition structure so that the desired column is part of the table
                    if myfamily[row][column]==desired_value:
                        print(myfamily[row])#return 1 for the game?
                    else:
                        continue
                else:
                    continue
    elif desired_column == desired_value:
        print("Tautology found!!")
        print("Invoking the protection 'with_sqli_tautology_prevention'")
        print("Possible SQLi thwarted, please check this proposition",prop)#return 0 for the game?
        print("Verifying the tautology as a cycle in the graph, which will be the marker to say there's an attack")
        my_graph.add_weighted_edges_from([(desired_value,desired_column,2.0)])
        for cycle in nx.simple_cycles(my_graph):
            print(cycle)
        if len(cycle) > 0:
            print("Verified that an SQL Injection attack was attempted and was blocked. Found",len(cycle),"cycle(s) in the graph of statements in the proposition.")
        print_my_graph()
    else:
        print("Invoking the protection 'with_sqli_tautology_prevention'")
        print("Ran into some unexpected issue")#return 0 for the game?

#Defining main function 
def main(): 
    print("-------------------------select * from myfamily----------------------------")
    #Simulating "select * from myfamily"
    select_statement("*","Nil")
    print("-------------------------select * from myfamily where name=variable----------------------------")
    #Simulating "select * from myfamily where name=variable"
    select_statement("*", "name=A")
    print("-------------------------select * from myfamily where name=variable OR 1=1----------------------------")
    #simulating a classic SQL injection "select * from myfamily where name=variable OR 1=1"
    select_statement("*", "name=B OR 1=1")

# Using the special variable  
# __name__ 
if __name__=="__main__": 
    main() 