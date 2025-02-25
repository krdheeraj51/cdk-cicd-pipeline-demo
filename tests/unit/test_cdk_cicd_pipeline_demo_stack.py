import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_cicd_pipeline_demo.cdk_cicd_pipeline_demo_stack import CdkCicdPipelineDemoStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_cicd_pipeline_demo/cdk_cicd_pipeline_demo_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkCicdPipelineDemoStack(app, "cdk-cicd-pipeline-demo")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
