# Cleans workspace
?rm

# Setting up packages on our workspace
library('neuralnet')

# Setting directory to get the file
setwd('/home/anirudt/Projects/iquest/')
directory <- getwd()
dat <- read.csv(paste(directory,'/parkinsons.data', sep=""), header = TRUE, sep = ",")

# Removing the 'name' column
features_total <- dat[,-1]
# Removing the status column
features_total <- features_total[,-17]

# Our training vector
status <- dat[,18]

features_train = features_total[1:150,]
status_train = status[1:150]

train <- data.frame(features_train, status_train)
n <- names(train)
f <- as.formula(paste('status_train ~', paste(n[!n %in% 'status_train'], collapse = ' + ')))

# ***********************************
# Making the model, some instructions
# ***********************************

# use hidden = c(x,y) to have x and y no. of neurons in 1st and 2nd hidden layers
# tweak with the parameters for better results, use help(neuralnet) for more.
net <- neuralnet(f, train, hidden = 10, threshold=0.01)

test_features <- features_total[150:nrow(features),]
status_test = status[150:length(status)]
net.results <- compute(net, test_features)
print(net.results$net.result)

result <- (net.results$net.result > 0.5)

print("Number of false reports:")
flaws <- sum(result!=status_test)
print(flaws)
