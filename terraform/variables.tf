variable "image_name" {
  description = "Name of the Docker image to build/use"
  type        = string
  default     = "dataops-pipeline"
}

variable "container_name" {
  description = "Name of the Docker container"
  type        = string
  default     = "dataops-pipeline-container"
}