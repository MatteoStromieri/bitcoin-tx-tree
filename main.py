import transaction, helpers, tree_builder, tree_visualizer
import matplotlib

def main():
    
    #ciclo da eseguire fin quando l'utente non ci da "exit"(lascia blank) in input
    while(True):
        # transaction retrieval
        tx_id = input("Insert a transaction ID or leave blank to close the program: ")
        if tx_id == "":
            break
        try:
            tx = helpers.get_tx(tx_id)
        except Exception as e:
            print("An error occured, maybe you didn't enter a correct input")
            continue
        # height 
        height = input("Insert the maximum height (if this space is left blank, the program will compute the full history of the TX, which can take a long time):")
        try:
            height = int(height)
            height_bool = True
        except Exception as e:
            print("...The program will compute the full history of the TX")
            height_bool = False
        # transaction parsing
        if transaction.SegWitTx.isSegWit(tx):
            tx = transaction.SegWitTx.parse(tx, tx_id)
        else:
            tx = transaction.Tx.parse(tx, tx_id)
        # tree building
        if height_bool == True:
            tree = tree_builder.TreeBuilder.buildTree(tx, height)
        else:
            tree = tree_builder.TreeBuilder.buildTree(tx)
        # visualize tree
        nx_tree = tree_visualizer.build_nx_tree(tree)
        tree_visualizer.visualize_tree(nx_tree)
    return

# sample transaction: 5e86b6609207e3376ebddde5e96da2b33ccfba3783f2389cb2aaad6452be985d
if __name__=="__main__":
    matplotlib.use('TkAgg')
    main()