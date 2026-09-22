resource "docker_image" "pipeline" {
  name         = var.image_name
  keep_locally = true
}

resource "docker_container" "pipeline" {
  name  = var.container_name
  image = docker_image.pipeline.image_id
}