import numpy as np
import scipy.stats as st

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
        self.inv = False

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
        
    def insert(self, samp_id, key, population, weights = [], numcycles = 0):
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
                if len(weights) == 0:
                    self.insert(samp_id, np.random.choice(population), population, numcycles = numcycles+1) #rehash if the image already contains the sample
                else:
                    self.insert(samp_id, np.random.choice(population, p = weights), population, weights, numcycles+1)
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
            print("\nNode count: " + str(self.calc_listlen(key)), end = "")
            print("\n-------------------------")

    def invTable(self, nsamps):
        """
        Given a hash table mapping images to samples (self), reverses the table so that samples
        map to images. The inverted hash table is returned, meaning that this method does not
        modify HashTable self (does not modify in place).

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
        output.inv = True
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
            s_id  (int): Either the sample id for a HashTable mapping images to samples, or
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
    
    def find_longest_chain(self):
        """
        Given a HashTable mapping images to samples or samples to images (self),
        finds the longest chain of nodes that are linked to a particular key.

        Input: 
            None

        Output: 
            Tuple of size two (first element is index position, second
            element is the number of nodes make up the longest chain)
        """
        maximum = 0
        maxind = []
        for key in self.table.keys():
            current = self.table[key]
            counter = 0
            while current != None:
                current = current.next
                counter += 1
            if counter > maximum:
                maximum = counter
                maxind = [key]
            elif counter == maximum:
                maxind.append(key)
        return (maxind, maximum)
    
    def show_stats(self):
        """
        Prints stats regarding the HashTable self.

        Input:
            None

        Output:
            None
        """
        print("Nodes: " + str(self.numelements))
        print("Keys: " + str(self.n_buckets))
        self.load_factor()
        info = self.find_longest_chain()
        print("Longest Chain: " + str(info[1]) + " at keys " + str(info[0]))
        print("HashTable Inverted? " + str(self.inv))
        
    def count_repeats(self):
        """
        Returns a tuple of size 2 containing information about images
        that are sampled more than once. The first element of the tuple is
        the number of duplicate entries. The second element of the tuple is a
        dictionary with each image ID as keys and the number of times that
        a duplicate sample was taken of that image.

        Input:
            None
        
        Output: Tuple of size two (first element is the number of duplicate entries,
        second element is a dictionary containing frequencies of duplicates by image
        ID.
        """
        inv_table = None
        if self.inv == False:
            inv_table = self.invTable(self.numelements)
        else:
            inv_table = self
        agglst = []
        for key in inv_table.table.keys():
            current = inv_table.table[key]
            while current != None:
                agglst.append(current.key)
                current = current.next
        dupls = {}
        unique = set(agglst)
        for element in unique:
            count = 0
            for i in agglst:
                if element == i:
                    count += 1
            if count != 1:
                dupls[element] = count - 1
        global_count = 0
        for val in dupls.values():
            global_count += val
        return (global_count, dupls)

    def move_node(self, src_img, dest_img, sample_id):
        """
        Given a source image, destination image, and a sample_id, moves the according node
        from the source image bucket to the destination image bucket.

        Input:
            src_img - int
            dest_img - int
            sample_id - int
        
        Output: None
        """
        current = self.table[src_img]
        rev_node = None
        if current == None:
            raise Exception("No samples have chosen this image.")
        if current.next == None and sample_id == current.key:
            rev_node = Node(current.key)
            self.table[src_img] = None
        elif current.next == None and sample_id != current.key:
            raise Exception("The sample requested does not appear in the image.")
        else:
            prev = None
            while current != None:
                if sample_id == current.key:
                    rev_node = Node(current.key)
                    prev.next = current.next
                    break
                else:
                    prev = current
                    current = current.next
            if current == None:
                raise Exception("The sample requested does not appear in the image.")
        current = self.table[dest_img]
        if current == None:
            self.table[dest_img] = rev_node
        else:
            while current.next != None:
                current = current.next
            current.next = rev_node
    
    def calc_listlen(self, img_id):
        """
        Determines the number of samp,les that have drawn a particular image.

        Input:
            img_id - int
        
        Output: count - int
        """
        count = 0
        current = self.table[img_id]
        while current != None:
            count += 1
            current = current.next
        return count

    def calc_avg_dupls(self):
        """
        Calculates the average length of duplicates in the hash table.

        Input:
            None
        Output:
            float
        """
        info = self.count_repeats()
        count = 0
        for i in info[1].values():
            count += i
        try:
            return count / len(info[1])
        except ZeroDivisionError:
            raise Exception("No duplicate entries in hash table.")

    def balance_leaves(self, num_iter):
        """
        Performs num_iter iterations of balancing, where nodes from a heavily-populated
        bucket are moved to a less heavily-populated bucket. Note that this does not
        change the load factor.

        Input:
            num_iter - Number of balancing iterations
        
        Output: None
        """
        for i in range(num_iter):
            dupls = self.count_repeats()
            avg = self.calc_avg_dupls()
            src_lst = []
            dest_lst = []
            for img_id in self.table.keys():
                if self.calc_listlen(img_id) <= avg - 1:
                    dest_lst.append(img_id)
            for img_id, num_dupl in dupls[1].items():
                if self.calc_listlen(img_id) >= avg + 1:
                    src_lst.append(img_id)
            for i,img_id in enumerate(src_lst):
                if i > len(dest_lst) - 1:
                    return
                else:
                    current = self.table[src_lst[i]]
                    while current.next != None:
                        current = current.next
                    self.move_node(src_lst[i], dest_lst[i], current.key)

    def img_load_dict(self):
        """
        Returns a dictionary with image ids as keys and the number of draws that
        have selected said image ids as values.

        Input:
            None
        
        Output: res - dict
        """
        res = {}
        for img in self.table:
            res[img] = self.calc_listlen(img)
        return res
    
    def img_load_stats(self):
        """
        Returns a dictionary with statistics about the hash table.

        Input: None

        Output: stat_res - dict
        """
        load_dict = self.img_load_dict()
        arr = []
        stat_res = {}
        for val in load_dict.values():
            arr.append(val)
        stat_res["Median"] = np.median(arr)
        stat_res["Mean"] = np.mean(arr)
        stat_res["Stdev"] = np.std(arr)
        stat_res["IQR"] = st.iqr(arr)
        stat_res["Lower Quartile"] = np.percentile(arr, 25)
        stat_res["Upper Quartile"] = np.percentile(arr, 75)
        stat_res["Max"] = max(arr)
        stat_res["Min"] = min(arr)
        return stat_res

    def find_outliers(self):
        """
        Uses the 1.5*IQR rule to find image ids that are outliers in terms
        of how many draws have chosen that particular image.

        Input: None

        Output: img_lst - list
        """
        img_lst = []
        nums = self.img_load_dict()
        stat_res = self.img_load_stats()
        for img_id,val in nums.items():
            if (val < stat_res["Lower Quartile"] - 1.5 * stat_res["IQR"] or
                val > stat_res["Upper Quartile"] + 1.5 * stat_res["IQR"]):
                img_lst.append(img_id)
        return img_lst

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
    inweights = input("Weights of each image (separate by commas)\n")
    weights = []  
    if inweights != "":
        strweights = list(inweights.split(","))
        for strw in strweights:
            try:
                weights.append(float(strw))
            except Exception:
                raise ValueError("Weights cannot be converted to integers")
        if len(weights) != len(population):
            raise Exception("Length of weights unequal to population size.")
        if (sum(weights) != 1):
            raise Exception("Sum of weight probabilities unequal to 1.")
    results.init_table(population)
    for samp_id in range(1,nsamples+1):
        if weights != []:
            choices = np.random.choice(population, samplesize, p = weights)
        else:
            choices = np.random.choice(population, samplesize)
        print("Selected images of sample " + str(samp_id) + ": " + str(choices))
        for i in choices:
            if weights != []:
                results.insert(samp_id, i, population, weights)
            else:
                results.insert(samp_id, i, population)
    #results.load_factor()
    #results.print_hash()
    invresults = results.invTable(nsamples)
    print(invresults.img_load_dict())
    print(invresults.img_load_stats())
    print(invresults.find_outliers())
    #invresults.del_sample(20)
    #invresults.print_hash_inv()
    #invresults.load_factor()
    #results.balance_leaves(100)
    #results.print_hash()
    #invresults = results.invTable(nsamples)
    #invresults.print_hash_inv()

if __name__ == "__main__":
    main()
