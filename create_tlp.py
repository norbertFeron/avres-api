from tlp_graph.create_tlp import create_tlp

if __name__ == '__main__':
    creator = create_tlp()
    creator.create_full()
    print("Tulip graph as been created from database")
