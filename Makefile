.PHONY: build push test sh

version := latest
IMAGE := metrics-python

build:
	docker build -t $(IMAGE):latest .

push: build
	docker tag $(IMAGE):latest ikerry/$(IMAGE):$(version)
	docker push ikerry/$(IMAGE):$(version)

test: build
	docker run --rm \
	 -w /app \
	 $(IMAGE):latest make test_in

sh: build
	docker run --rm -it \
		-w /app -v $(HOME)/.aws:/root/.aws \
	  -v $$(pwd):/app	\
		$(IMAGE):latest bash

test_in:
	green ./tests/
