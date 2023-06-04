import numpy as np

class Node:
    def __init__(self, key):
        """
        Constructor of the Node class.
        Each Node object will contain the key (the sample ID) and a
        pointer to the next node. Each distinct data point in a sample
        will occupy its own Node object. The HashTable class links these
        nodes with the image IDs.
        """
        self.key = key
        self.next = None

class HashTable:
    def __init__(self):
        """
        Constructor of the HashTable class.
        The HashTable is based off a dictionary (self.table) that links
        keys to values. The keys are the Image IDs, while the values are the
        Sample IDs. 

        Attributes:
            table - The hash table linking Image IDs to Sample IDs
            numelements - Number of elements in the hash table
            n_buckets - Number of image IDs that the hash table contains
        """
        self.table = {}
        self.numelements = 0
        self.n_buckets = None

    def init_table(self, population):
        """
        Populates the table by creating keys corresponding to each
        image ID. Since no samples have been processed, each key points to
        None.

        Input:
            population (list) - A list of image IDs
        
        Output:
            None
        """
        self.n_buckets = len(population)
        for i in population:
            self.table[i] = None
        
    def insert(self, samp_id, key, population, numcycles = 0):
        """
        Given a sample ID and an image ID (which is the hash table key), inserts
        a Node containing the sample_id into the hash table.

        Input:
            samp_id (int) - The ID of a specific sample
            key (int) - The image ID
            population (list) - The population of image IDs
            numcycles (int) - Number of rehashes needed to ensure that the sample
            does not contain repeat data points
        
        Output:
            None
        """
        flag = False
        current = self.table[key]
        if current == None:
            flag = True
        prev = None
        while (current != None):
            if (current.key == samp_id and numcycles < 100):
                self.insert(samp_id, np.random.choice(population), population, numcycles+1) #rehash if the image already contains the sample
                return
            elif (current.key == samp_id and numcycles >= 100):
                raise Exception("Too many rehashes.")
            prev = current
            current = current.next
        current = Node(samp_id)
        if flag:
            self.table[key] = current
        if (prev != None):
            prev.next = current
        self.numelements += 1

    def load_factor(self):
        """
        Computes and prints the load factor, which is the number of elements in the hash
        divided by the number of buckets (how many images are in the population).

        Input:
            None
        
        Output:
            None
        """
        print("Load Factor: " + str(self.numelements / self.n_buckets))

    def print_hash(self):
        """
        Displays the hash table. For each bucket (image ID), shows how many sample
        IDs are linked to that particular image ID.

        Input:
            None
        
        Output:
            None
        """
        print("-------------------------")
        for key,node in self.table.items():
            print("Image ID: " + str(key))
            current = node
            print("Sample IDs:", end = " ")
            while (current != None):
                print(str(current.key), end = " ")
                current = current.next
            print("\n-------------------------")

    def invTable(self, nsamps):
        """
        Given a hash table mapping images to samples (self), reverses the table so that samples
        map to images.

        Input:
            nsamps (int) - number of samples
        
        Output:
            output (HashTable)
        """
        samplepop = list(np.arange(1,nsamps+1))
        output = HashTable()
        output.init_table(samplepop)
        for img in self.table.keys():
            current = self.table[img]
            while (current != None):
                csamp = current.key
                output.insert(img, csamp, samplepop)
                current = current.next
        output.n_buckets = nsamps
        return output

    def print_hash_inv(self):
        """
        Given an inverted hash table, prints sample-image pairs.

        Input:
            None
        
        Output:
            None
        """
        print("-------------------------")
        for key,node in self.table.items():
            print("Sample ID: " + str(key))
            current = node
            print("Image IDs:", end = " ")
            while (current != None):
                print(str(current.key), end = " ")
                current = current.next
            print("\n-------------------------")

    def del_sample(self, s_id):
        """
        Given a HashTable mapping images to samples or samples to images (self),
        deletes all nodes in the HashTable that share the same value as s_id.
        For a HashTable mapping images to samples, del_sample takes in a sample id
        and deletes all instances of that sample in the HashTable.
        For a HashTable mapping samples to images, del_sample takes in an image id
        and deletes all instances of that image in the HashTable.

        Input:
            s_id  (int) - Either the sample id for a HashTable mapping images to samples, or
            the image id for a HashTable mapping samples to images.
        
        Output:
            None
        """
        for key in self.table.keys():
            current = self.table[key]
            if current == None:
                continue
            elif current.key == s_id:
                self.table[key] = current.next
                self.numelements -= 1
            else:
                prev = None
                while (current != None and current.key != s_id):
                    prev = current
                    current = current.next
                if (current != None):
                    prev.next = current.next
                    self.numelements -= 1

#Testing Functionalities of HashTable class
def main():
    try:
        datasize = int(input("Dataset size:\n"))
        population = np.arange(1, datasize+1)
        samplesize = int(input("Sample size:\n"))
        nsamples = int(input("Number of samples:\n"))
    except Exception:
        print("Invalid input")
    results = HashTable()
    results.init_table(population)
    for samp_id in range(1,nsamples+1):
        choices = np.random.choice(population, samplesize)
        print("Selected buckets: " + str(choices))
        for i in choices:
            results.insert(samp_id, i, population)
    results.print_hash()
    results.load_factor()
    print(results.numelements)
    results.del_sample(5)
    results.print_hash()
    results.load_factor()
    print(results.numelements)
    invresults = results.invTable(nsamples)
    invresults.del_sample(20)
    invresults.print_hash_inv()
    invresults.load_factor()
if __name__ == "__main__":
    main()
