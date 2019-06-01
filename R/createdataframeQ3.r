
library(jsonlite)
library(parallel)

#import data
cl <- makeCluster(detectCores() - 1)
json_files<-list.files(path="C:\\Users\\danie\\Desktop\\spark\\StreamingData\\Unstructured/", recursive=T, pattern="part*", full.names=T)
json_list<-parLapply(cl,json_files,function(x) rjson::fromJSON(file=x,method = "R"))
stopCluster(cl)

#create dataframe
df <- data.frame(matrix(unlist(json_list), nrow=length(json_list), byrow=T))

#rename col
names(df) <- c("book_title", "review_title", "review_user", "book_id", "review_id", "timestamp", "review_text", "review_score")

#convert222
df$book_title <- as.character(df$book_title)
df$review_title <- as.character(df$review_title)
df$review_user <- as.character(df$review_user)
df$book_id <- as.character(df$book_id)
df$review_id <- as.character(df$review_id)
df$timestamp <- as.character(df$timestamp)
df$review_text <- as.character(df$review_text)
df$review_score <- as.integer(df$review_score)

#remove duplicates 
df2 <- df[!duplicated(df$review_text),]

#write csv
write.csv(df2, file = "C:\\Users\\danie\\Documents\\Daniel Gil\\KULeuven\\Stage 2\\Term 2\\Advanced Analytics\\Assignments\\Streaming\\Data/bookdataDaniel.csv")

#import data check
datacheck <- read.table("C:\\Users\\danie\\Documents\\Daniel Gil\\KULeuven\\Stage 2\\Term 2\\Advanced Analytics\\Assignments\\Streaming\\Data/bookdataDaniel.csv", header=TRUE, sep=",")
#works
View(head(datacheck))


