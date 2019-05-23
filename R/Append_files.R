setwd("C:\\Users\\danie\\Desktop\\spark\\Data")

files <- list.files()
files

file1 <- read.csv(files[1],sep = ",")
file2 <- read.csv(files[2],sep = ",")
file3 <- read.csv(files[3],sep = ",")

#length(unique(file1$review_id))
#length(unique(file2$review_id))
#length(unique(file3$review_id))
file2 <- file2[!duplicated(file2$review_id),]

all.equal(colnames(file1), colnames(file2))
all.equal(colnames(file2), colnames(file3))

file_all <- rbind(file1, file2, file3)
file_all$X <- seq(1:nrow(file_all))
View(head(file_all))

file_all2 <- file_all[!duplicated(file_all[,-1]),]

write.csv(file_all2, "data.csv", row.names = F)

test <- read.csv("data.csv",sep = ",")
names(test)
?read.csv

table(file1$review_score, useNA = "always")
table(file2$review_score, useNA = "always")
table(file3$review_score, useNA = "always")
table(test$review_score, useNA = "always")

View(head(test))
View(test[test$X == 32,])
View(test[test$review_id == 'R1DTLSSGUP2QHR',])
View(file2[file2$review_id == 'R1DTLSSGUP2QHR',])
