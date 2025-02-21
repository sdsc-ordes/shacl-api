import subprocess


def runInferenceTest():
    output = subprocess.run(
        [
            "shaclinfer.sh",
            "-datafile",
            "tests-files/inf_imagingID.ttl",
            "-shapesfile",
            "tests-files/inf_ImagingOntologyShapes.ttl",
        ],
        stdout=subprocess.PIPE,
    )

    with open("inferenceTest.ttl", "wb") as f:
        f.write(output.stdout)


runInferenceTest()
