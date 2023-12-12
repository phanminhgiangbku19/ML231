import os
# path joining version for other paths
DIR = '/Users/macbook/documentOfKhanh/google_download/test/result/safe'
print(len([name for name in os.listdir(DIR)
      if os.path.isfile(os.path.join(DIR, name))]))
