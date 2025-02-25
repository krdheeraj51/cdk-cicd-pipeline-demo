from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as _lambda,
    aws_codebuild as codebuild,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as cpactions,
    SecretValue
)
from constructs import Construct

class CdkCicdPipelineDemoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

         # Create Lambda Function
        lambda_function = _lambda.Function(
            self, "MyLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset("lambda")
        )

        # Create a CodeBuild Project
        build_project = codebuild.PipelineProject(
            self, "BuildProject",
            build_spec=codebuild.BuildSpec.from_object({
                "version": "0.2",
                "phases": {
                    "install": {
                        "runtime-versions": {"python": "3.8"},
                        "commands": ["pip install -r requirements.txt"]
                    },
                    "build": {
                        "commands": ["echo 'Building the package'"]
                    }
                },
                "artifacts": {"files": ["**/*"]}
            })
        )

        # GitHub Source
        source_artifact = codepipeline.Artifact()
        build_artifact = codepipeline.Artifact()
        oauth_token = SecretValue.secrets_manager('github_cicd_accesss_secure_token')

        source_action = cpactions.GitHubSourceAction(
            action_name="GitHub_Source12",
            owner="krdheeraj51",
            repo="cdk-cicd-pipeline-demo",
            oauth_token=oauth_token,
            output=source_artifact,
            branch="main",
            trigger=cpactions.GitHubTrigger.WEBHOOK
        )

        # CodeBuild Action
        build_action = cpactions.CodeBuildAction(
            action_name="Build",
            project=build_project,
            input=source_artifact,
            outputs=[build_artifact]
        )

        # Deploy Action
        deploy_action = cpactions.LambdaInvokeAction(
            action_name="DeployLambda",
            lambda_=lambda_function
        )

        # Define CodePipeline
        pipeline = codepipeline.Pipeline(
            self, "Pipeline",
            stages=[
                codepipeline.StageProps(stage_name="Source", actions=[source_action]),
                codepipeline.StageProps(stage_name="Build", actions=[build_action]),
                codepipeline.StageProps(stage_name="Deploy", actions=[deploy_action])
            ]
        )

