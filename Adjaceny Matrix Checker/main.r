adjacencymatrix <- function(sample){
  sample <- na.omit(sample)
  test1 <- length(sample) == length(sample[,1])
  # is square
  temp <- 0
  for (x in sample){
    temp <- temp + length(x[x != 1 && x !=0])
  }
  test2 <- temp[1] == 0
  #only 0 and 1s
  
  test3 <- TRUE
  for (x in seq(1,length(sample))){
    test3 <- test3 && (sample[x,x] == 0)
  }
  # diagonal only 0
  
  test4 <- TRUE
  for(x in (t(sample) == sample)){
    test4 <- test4 && Reduce(function(x,y) {x && y}, x, TRUE)
  }
  #survives being transposed
  return (test1 && test2 && test3 && test4)
}