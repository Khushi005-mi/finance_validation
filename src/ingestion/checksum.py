# imports
import hashlib
import os 

## CHECKSUM GENERATION FUNCTION
def checksum_generate(file_path: str) -> str:
    """Generates a checksum for a given file using SHA-256 algorithm.

    Args:
        file_path (str): The path to the file for which the checksum is to be generated.

    Returns:
        str: The generated checksum as a hexadecimal string.
    """
     # 1️⃣ Validate file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
      # 2️⃣ Create MD5 hash object
    hash_md5 = hashlib.md5()



      # 3️⃣ Read file in chunks (memory-safe for large files)
    with open(file_path , "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
       # 4️⃣ Return hexadecimal checksum
    return hash_md5.hexdigest()

    # DUPLICATE FILE DETECTION
def check_duplicate(file_path:str , checksum_store: dict):
        """Checks if a file is a duplicate based on its checksum.

        Args:
            file_path (str): The path to the file to be checked.
            checksum_store (dict): A dictionary storing previously generated checksums.

        Returns:
            bool: True if the file is a duplicate, False otherwise.
        """
     # 1️⃣ Generate checksum for current file
        checksum = checksum_generate(file_path)
       # 2️⃣ Check if checksum already exists
        if checksum in checksum_store:
          return True
      # 3️⃣ Store checksum and mark as new file
        
        checksum_store.add(checksum)
        return False

        # LOCAL TEST / DEMO RUN
if __name__ == "__main__":
    path = "data/corrupted/your_file.csv"
 # 1️⃣ Generate and print checksum
    checksum = checksum_generate(path)
    print(f"Checksum: {checksum}")
  # 2️⃣ Test duplicate detection logic
    seen = set()
    print(f"First load duplicate? {check_duplicate(path, seen)}")
    print(f"Second load duplicate? {check_duplicate(path, seen)}")