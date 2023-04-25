# lambda-gtp
Add an OpenAI LLM to your web application using an AWS lambda function.

Content
- [Background](#background)
- [Cost](#cost)
- [How To](#how-to)

## Background
AWS lambda functions are a very convenient and cost effective way to create a serverless API for your website.

When I started building my personal website, I was trying to find every method to make what was a static website feel as dynamic as possible. This is very easy to do, as long as you're using public APIs! Really all you need to do is ask ChatGPT to write a static website to your liking, insert some free APIs (like quotes, stock prices, etc.), then have GitHub pages host it. All for $0!

Now you may have found some amazing potential to integrate AI into your website like I did, especially now that OpenAI has a public API available. Then you realize it's behind a paywall, and if you do decide to pay for it you, now you'll have a secret API key that you definitely don't want other people to know about or else you'll be paying much much more than $0! 

You may be thinking, "oh great now I'll have to build a server just to keep this information safe." While this may be optimal for large websites, this defeats the point for smaller websites who likely chose to go static because you wanted it to be low maintenance. This is where AWS lambda functions can save the day! 

## Cost
Here's a small breakdown for the pricing that might help give an idea of how much you might be paying to use OpenAI's API and AWS Lambda with an optional custom domain name. 
- [gpt-3.5-turbo](https://openai.com/pricing) | $0.002 / 1K tokens (~ 750 words)
- [AWS Lambda](https://aws.amazon.com/lambda/pricing/) | First 6 Billion GB-seconds / month | $0.0000166667 for every GB-second | $0.20 per 1M requests
- [Custom Domain Name](https://www.godaddy.com/pricing) | ~ $20 / year

Looking at these numbers, gpt-3.5-turbo and AWS Lambda are cheaper than a custom domain name! So if you scrap the domain name and stick with what github gives you, something.github.io, then it's pocket change! 

## How To
If you've read through all of that and find yourself with a similar story then this repository will provide you with the template and references required to include any OpenAI LLM to your website using AWS Lambda functions. It's assumed you already have a website and know how and where you're going to make these API calls. This, How To, will help you lay down the infrastructure for your serverless API.

1. Create a new Lambda Function with the name of your endpoint.
2. Copy all of the code from the [lambda_function.py](https://github.com/hiyaryan/lambda-gpt/blob/main/src/lambda_function.py) file in this repository and paste it into the code block of your AWS Lambda Function you just created.

    You should update this piece of code to your liking. You can play around with the settings and which LLM you'd like to use at OpenAI's [playground](https://platform.openai.com/playground) before committing (of course this can be changed anytime you like).

    ```py
        # Call the OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
    ```

3. In your AWS account under the Lambda Function service (assuming you're already there), go to your **Configuration** tab and click on ***Environment variables***. This is where you'll insert your `OPENAI_API_KEY` that you want to protect.

    3.1. Go get your [OpenAI API Key](https://platform.openai.com/account/api-keys), and copy the long string of characters before you close the window (it only shows once so make sure you copy and paste it somewhere safe). 
    
    3.2. Go back to your AWS account and insert the key into the value section. You can simply same the key `OPENAI_API_KEY`. This name should match that in the code (shown below) of which you copied into your lambda function.

    ```py
    # Set up the OpenAI API client
    openai.api_key = os.environ['OPENAI_API_KEY']
    ```

4. If you try to test this function now, it will fail because AWS does not include the `openai` module in its Python runtime environment. So you need to create a **Layer** that you'll upload this module to.

    4.1 Now, I will refer you to this LinkedIn post that I use to create a Lambda Layer. One thing that you will need to do differently though is instead of `pandas` you'll run `pip install openai -t .` 
    
    Note that for this step you'll need to create an [AWS S3 Bucket](https://s3.console.aws.amazon.com/s3/buckets?region=us-west-1) to store the external modules in if you follow this tutorial (this should be free for individuals, it was free for me). Just make sure it's created in the same region as your Lambda Function.

    AWS Lambda Layers Tutorial: [Add External Python Libraries to AWS Lambda using Lambda Layers](https://www.linkedin.com/pulse/add-external-python-libraries-aws-lambda-using-layers-gabe-olokun%3FtrackingId=uEcLp89cRZGqILgGevDEyw%253D%253D/?trackingId=uEcLp89cRZGqILgGevDEyw%3D%3D)

    4.1.2. Alternatively (I recommend following 4.1 as I have not tested this but it should work in theory), you could upload the [package.zip](https://github.com/hiyaryan/lambda-gpt/blob/main/src/package.zip) file that I created which is essentially what you'll be creating inside an AWS Cloudshell instance from the tutorial above (some steps may vary)

    `package.zip` contains `lambda_function.py`, the `openai` module and all of the modules that were installed to support it.

    Side note, from a security perspective, I wouldn't upload some random looking zip file into my Lambda Function which is what we're creating because we want to secure our OpenAI API key *even though this package.zip is safe* (anyone can say that though).

5. After following that essential step, everything should be working! But if you're trying to figure out what json test you should pass, allow me to give you this test that I asked ChatGPT for,

    ```json
    {
        "input": "What is the capital of France?"
    }
    ```

    If it's working properly, well, you should get back Paris... or the hallucinated capital of France from ChatGPT (just kidding, ChatGPT wouldn't do that on its first message)!