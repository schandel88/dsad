#!/usr/bin/env python
# coding: utf-8

# In[4]:


import os

# BankNode is used to create Bank objects with fields like bank_name, note_count, month. Heap will also be storing BankNode objects  
class BankNode:
    def __init__(self, bank_name, note_count, month):
        self.bank_name = bank_name
        self.note_count = note_count
        self.month = month

# MaxHeap class implements max heap and supports insert, delete and print operations.         
class MaxHeap:
    # Initialise the Max Heap with the size as capacity, which will be passed wihle creating instances.
    def __init__(self, capacity):
        self.capacity = capacity
        self.heap = []
    
    def parent(self, i):
        return (i - 1) // 2
    
    # Returns the index of left child of ith element.
    def left_child(self, i):
        return 2 * i + 1
    
    # Returns the index of right child of ith element.
    def right_child(self, i):
        return 2 * i + 2
    
    # This function is used to swap elements present at ith and jth loctions.
    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    # Insert function is used to insert new BankNodes to Max Heap, while maintaing the max heap property.
    def insert(self, node):
        if len(self.heap) == self.capacity:
            raise Exception("Heap is full")
        
        self.heap.append(node)
        current_index = len(self.heap) - 1
        
        # Maintain the max heap property by comparing the node with its parent
        while current_index > 0 and self.heap[current_index].note_count > self.heap[self.parent(current_index)].note_count:
            self.swap(current_index, self.parent(current_index))
            current_index = self.parent(current_index)
    
    # Delete function is used to remove the max BankNode which has highest number of 2000 Rs notes. It then returns that node.
    def delete(self):
        if len(self.heap) == 0:
            raise Exception("Heap is empty")
        
        deleted_node = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        
        # Restore the max heap property after deleting the root
        self.max_heapify(0)
        
        return deleted_node
    
    # This function is used after delete operation to maintain the max heap property
    def max_heapify(self, i):
        largest = i
        left = self.left_child(i)
        right = self.right_child(i)
        
        # Find the largest element among the current node and its children
        if left < len(self.heap) and self.heap[left].note_count > self.heap[largest].note_count:
            largest = left
        
        if right < len(self.heap) and self.heap[right].note_count > self.heap[largest].note_count:
            largest = right
        
        # Swap the current node with the largest child if necessary
        if largest != i:
            self.swap(i, largest)
            self.max_heapify(largest)
            
    # This function prints the max heap        
    def print_heap(self):
        heap_str = ""
        for node in self.heap:
            heap_str += f"{node.bank_name}, {node.note_count}, {node.month}\n"
        return heap_str

# This function is used to remove all the blank lines while reading from file   
def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line          

# We initialise the 2 max heaps of size hundered for may and june months           
may_heap = MaxHeap(100)
june_heap = MaxHeap(100)
filename = 'inputPS07.txt'
entry_list = []
new_bank_entry_list = []
try:
    # Open the file in read mode
    with open(filename, 'r') as file:
        # Read each line in the file
        new_bank_details = False
        
        for line in nonblank_lines(file):
            # Skip the header line
            if (line.strip().lower() == 'bank name, note count, month'):
                continue
                
            if (line.strip().lower() == 'new bank details:'):
                new_bank_details = True
                continue
            
            # Split the line by comma to separate the fields and create a dictionary entry
            fields = line.strip().split(',')
            entry = {"bank_name": fields[0].strip(),"note_count": int(fields[1].strip()),"month": fields[2].strip()}

            # Append the entry to the appropriate list based on new_bank_details flag
            if(new_bank_details == False):
                entry_list.append(entry)
            else:
                new_bank_entry_list.append(entry)
            
# Handling exception for file not found and 2nd one will handle all data related exceptions.
except FileNotFoundError:
    print("File not found. Please check the file name and path.")
except Exception as e:
    print("An error occurred while reading the file:", str(e))      
            
try:            
    # Check if output file already exits and remove that, if present   
    output_filename = 'outputPS07.txt'
    if os.path.exists(output_filename):
        os.remove(output_filename)
    with open(output_filename, 'w') as output_file:
        
        # Write the May month details to the output file
        output_file.write('May month Details\n')
        print('May month Details\n')
        total_may = 0
        # Iterate the entry_list, check and print all May month entries.
        for i1 in entry_list:
            if(i1['month'].lower() == 'may'):
                print(i1)
                output_file.write(i1['bank_name'] + ',' + str(i1['note_count'])+'\n')
                heap_entry = BankNode(i1['bank_name'], i1['note_count'], i1['month'])
                may_heap.insert(heap_entry)
                total_may+=i1['note_count']
                
        
        total_june = 0
        # Write the June month details to the output file
        output_file.write('\nJune month Details\n')
        print('June month Details\n')
        # Iterate the entry_list, check and print all June month entries.
        for i2 in entry_list:
            if(i2['month'].lower() == 'june'):
                print(i2)
                output_file.write(i2['bank_name'] + ',' + str(i2['note_count'])+'\n')
                heap_entry = BankNode(i2['bank_name'], i2['note_count'], i2['month'])
                june_heap.insert(heap_entry)
                total_june+=i2['note_count']
        
        # Write the total note count for May and June to the output file
        output_file.write('\nTotal Rs 2000 note count for May & June month:' + str(total_may) + ' & ' + str(total_june) + '\n')

        # Write the new bank details to the output file
        output_file.write('\nAdded new bank details:\n')
        print('Added new bank details:\n')        

        for i3 in new_bank_entry_list:
            print(i3)
            output_file.write(i3['bank_name'] + ',' + str(i3['note_count']) + ',' + i3['month'] +'\n')
            
            if(i3['month'].lower() == 'may'):
                heap_entry = BankNode(i3['bank_name'], i3['note_count'], i3['month'])
                may_heap.insert(heap_entry)
                total_may+=i1['note_count']
                
            if(i3['month'].lower() == 'june'):
                heap_entry = BankNode(i3['bank_name'], i3['note_count'], i3['month'])
                june_heap.insert(heap_entry)
                total_may+=i1['note_count']
        
        # Delete the maximum amount deposited in May and June and write the details to the output file
        max_may_node = may_heap.delete()
        output_file.write('\nMaximum amount deposited in {0}: {1} for may month...\n'.format(max_may_node.bank_name, max_may_node.note_count))
        max_june_node = june_heap.delete()
        output_file.write('Maximum amount deposited in {0}: {1} for June month...\n'.format(max_june_node.bank_name, max_june_node.note_count))
        
        # Calculate the total amount collected so far in all banks and write it to the output file
        total_rs = (total_may + total_june)*2000
        output_file.write('\nTotal amount that collected so far in all the banks: Rs {0}\n'.format(total_rs))

        # Write the max heap for May and June to the output file
        output_file.write('\nMax Heap for May Month:\n')
        may_out = may_heap.print_heap()
        output_file.write(may_out)
        print(may_out)
        output_file.write('\nMax Heap for June Month:\n')
        june_out = june_heap.print_heap()
        output_file.write(june_out)
        print(june_out)
        
# Generic exception handling to catch all the file write related exceptions        
except Exception as e:
    print("An error occurred while writing to the file:", str(e))
  


# In[ ]:




