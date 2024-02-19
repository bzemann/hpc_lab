#include <iostream>
#include <limits.h>
#include <unistd.h>

int main(){
  char hostname[HOST_NAME_MAX];
  gethostname(hostname, HOST_NAME_MAX);
  std::cout << "Hostname: " << hostname << std::endl;
  std::cout << "Hello, World!\n";
  return 0;
}