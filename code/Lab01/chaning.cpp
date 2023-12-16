#include "readfile.h"

/* Hash function to choose bucket
 * Input: key used to calculate the hash
 * Output: HashValue;
 */
int firstHashfunction(int key) { return key % MBUCKETS; }
int secondHashfunction(int key) { return MBUCKETS - firstHashfunction(key); }

/* Functionality insert the data item into the correct position
 *          1. use the hash function to determine which bucket to insert into
 *          2. search for the first empty space within the bucket
 *          	2.1. if it has empty space
 *          	           insert the item
 *          	     else
 *          	          use OpenAddressing to insert the record
 *          3. return the number of records accessed (searched)
 *
 * Input:  fd: filehandler which contains the db
 *         item: the dataitem which should be inserted into the database
 *
 * Output: No. of record searched
 *
 * Hint: You can check the search function to give you some insights
 * Hint2: Don't forget to set the valid bit = 1 in the data item for the rest of
 functionalities to work
 * Hint3: you will want to check how to use the pwrite function using man pwrite
 on the terminal
 * 			 ssize_t pwrite(int fd, const void *buf, size_t count,
 off_t offset);
 *
 * 	pwrite() writes up to count bytes from the buffer starting  at  buf  to
       the  file  descriptor  fd  at  offset  offset.
 */
/***
 * @par fd file pointer to the output
 * @par item the item to be inserted
 * @return number of records accessed
 */
int ChainingHashing(int fd, DataItem &item) {
  int counter = 0;
  int offset = firstHashfunction(item.key)*sizeof(ListedBucket);
  ListedBucket bucket;
  auto result = pread(fd, &bucket, sizeof(ListedBucket), offset);
  if (result <= 0) {
	perror("some error occurred in pread");
	return -1;
  }
  // use the newNode to create a temporary node
  Node *newNode = (struct Node*) malloc(sizeof(struct Node));
  newNode->dataItem = item;
  newNode->next = nullptr;
  Node *prev = nullptr;
  Node *curr = bucket.head;
  if(curr == nullptr){
	bucket.head = newNode;
	// write the bucket back to the file
	if (pwrite(fd, &bucket, sizeof(ListedBucket), offset) <=0)
	{
	  perror("some error occurred in pwrite");
	  return -1;
	}
	return counter;
  }
  while(curr != nullptr){
	if(curr->dataItem.valid == 0 or curr->dataItem.valid == -1){
	  curr->dataItem.data = item.data;
	  return counter;
	}
	prev = curr;
	curr = curr->next;
	counter++;
}
// insert at the end of the linked list
if(prev != nullptr){
	prev->next = newNode;
}

	if (pwrite(fd, &bucket, sizeof(ListedBucket), offset) <=0)
	{
		perror("some error occurred in pwrite");
		return -1;
	}
  return counter;

}


int insertItem(int fd, DataItem item,int type) {
  int loc = firstHashfunction(item.key);
  // call the openAddressing
  return ChainingHashing(fd, item);
}

/* Functionality: using a key, it searches for the data item
 *          1. use the hash function to determine which bucket to search into
 *          2. search for the element starting from this bucket and till it find
 * it.
 *          3. return the number of records accessed (searched)
 *
 * Input:  fd: filehandler which contains the db
 *         item: the dataitem which contains the key you will search for
 *               the dataitem is modified with the data when found
 *         count: No. of record searched
 *
 * Output: the in the file where we found the item
 */

int searchItem(int fd, struct DataItem* item, int* count) {
    // Definitions
    struct DataItem data;   // a variable to read in it the records from the db
    *count = 0;             // No of accessed records
    int hashIndex = firstHashfunction(item->key);                // calculate the Bucket index
    int startingOffset = hashIndex * sizeof(ListedBucket);    // calculate the starting address of the bucket
    int Offset = startingOffset;                        // Offset variable which we will use to iterate on the db
    
    // Main Loop
    RESEEK:
    // Read the current bucket
    ListedBucket currentBucket;
    ssize_t readResult = pread(fd, &currentBucket, sizeof(ListedBucket), Offset);
    // One record accessed
  
    // Check whether it is a valid record or not
    if (readResult <= 0) {
        // Either an error happened in the pread or it hit an unallocated space
        // perror("some error occurred in pread");
        return -1;
    } else {
        // Search for the item in the linked list in the current bucket
        struct Node* currentNode = currentBucket.head;
        while (currentNode != NULL) {
            if (currentNode->dataItem.valid == 1 && currentNode->dataItem.key == item->key) {
                // Found the needed record
                item->data = currentNode->dataItem.data;
                return Offset;
            }
            currentNode = currentNode->next;
            (*count)++;
        }

        // Go back to the beginning if reached the end of the file
        if (Offset == startingOffset) {
            return -1; // Record not found
        }

        goto RESEEK;
    }
}


/* Functionality: Display all the file contents
 *
 * Input:  fd: filehandler which contains the db
 *
 * Output: no. of non-empty records
 */
int deleteOffset(int fd, int Offset, int keyToDelete) {
    // Definitions
    ListedBucket currentBucket;

    // Read the current bucket
    ssize_t readResult = pread(fd, &currentBucket, sizeof(ListedBucket), Offset);

    if (readResult < 0) {
        perror("Error occurred in pread");
        return -1;
    }

    // Search for the item in the linked list in the current bucket
    struct Node* currentNode = currentBucket.head;
    struct Node* prevNode = NULL;

    while (currentNode != NULL) {
        if (currentNode->dataItem.valid == 1 && currentNode->dataItem.key == keyToDelete) {
            // Found the needed record, set the valid bit to 0 to mark it as deleted
            currentNode->dataItem.valid = 0;

            // Write the updated bucket back to the file
            ssize_t writeResult = pwrite(fd, &currentBucket, sizeof(ListedBucket), Offset);
            if (writeResult < 0) {
                perror("Error occurred in pwrite");
                return -1;
            }

            return 0; // Successful deletion
        }

        prevNode = currentNode;
        currentNode = currentNode->next;
    }

    // The record to delete is not found in the current bucket
    return -1;
}

int DisplayFile(int fd) {
    int count = 0;
    int Offset = 0;

    for (Offset = 0; Offset < FILESIZE; Offset += sizeof(ListedBucket)) {
        // Read the current bucket
        ListedBucket currentBucket;
        ssize_t readResult = pread(fd, &currentBucket, sizeof(ListedBucket), Offset);

        if (readResult < 0) {
            perror("Error occurred in pread");
            return -1;
        }

        // Display information about the bucket
        printf("Bucket: %d, Offset: %d\n", Offset / BUCKETSIZE, Offset);

        // Display information about each item in the linked list
        struct Node* currentNode = currentBucket.head;
        while (currentNode != NULL) {
            if(currentNode->dataItem.valid != 0) 
                printf("  Data: %d, Key: %d\n", currentNode->dataItem.data, currentNode->dataItem.key);
            currentNode = currentNode->next;
            count++;
        }
    }

    return count;
}


