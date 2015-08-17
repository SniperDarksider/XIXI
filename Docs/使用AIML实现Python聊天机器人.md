原文：[AI Chat Bot in Python with AIML](http://devdungeon.com/content/ai-chat-bot-python-aiml)

通过AIML包，用Python很容易写出人工智能的聊天机器人。AIML代表人工智能修饰语言，但它仅是一个简单的XML。下面这些代码样例将带你了解如何使用Python创造你自己的人工智能聊天机器人。

# AIML是什么？
AIML是由Richard Wallace开发的。他制作了一个叫做A.L.I.C.E.（人工语言学网络计算机实体）的机器人，并获得了一些人工智能的奖项。有趣的是，找寻人工智能的图灵测试中的一项是，让一个人通过文字接口与一个机器人对话几分钟，然后看看他们是否把它当做一个人。AIML以XML的形式来定义匹配模式规则，然后决定应答。

获得完整的AIML入门，查看[Alice Bot's AIML Primer](http://www.alicebot.org/documentation/aiml-primer.html)。你将学到更多关于AIML的东西，以及在[AIML Wikipedia page](https://en.wikipedia.org/wiki/AIML)上看到它能够做什么。我们将首先创建AIML文件，然后使用Python给它赋予活力。

# 创建标准启动文件
标准的做法是，创建一个名为**std-startup.xml**的启动文件，作为加载AIML文件的主入口点。在这个例子中，我们将创建一个基础的文件，它匹配一个模式，并且返回一个相应。我们想要匹配模式**load aiml b**，然后让它加载我们的aiml大脑作为响应。我们将在一分钟内创建basic_chat.aiml文件。

		<aiml version="1.0.1" encoding="UTF-8">
			<!-- std-startup.xml -->

			<!-- Category是一个自动的AIML单元 -->
			<category>

				<!-- Pattern用来匹配用户输入 -->
				<!-- 如果用户输入 "LOAD AIML B" -->
				<pattern>LOAD AIML B</pattern>

				<!-- Template是模式的响应 -->
				<!-- 这里学习一个aiml文件 -->
				<template>
					<learn>basic_chat.aiml</learn>
					<!-- 你可以在这里添加更多的aiml文件 -->
					<!--<learn>more_aiml.aiml</learn>-->
				</template>
				
			</category>

		</aiml>
		
# 创建一个AIML文件
在上面，我们创建的AIML文件只能处理一个模式:**load aiml b**。当我们向机器人输入那个命令时，它将会尝试加载**basic_chat.aiml**。除非我们真的创建了它，否则无效。下面是你可以写进**basic_chat.aiml**的内容。我们将匹配两个基本的模式和响应。

		<aiml version="1.0.1" encoding="UTF-8">
		<!-- basic_chat.aiml -->
		<aiml>

			<category>
				<pattern>HELLO</pattern>
				<template>
					Well, hello!
				</template>
			</category>
			
			<category>
				<pattern>WHAT ARE YOU</pattern>
				<template>
					I'm a bot, silly!
				</template>
			</category>
			
		</aiml>
		
# 随机响应
你也可以像下面这样添加随机响应。它将在接受到一个以"One time I"开头的消息的时候随机响应。*是一个匹配任何东西的通配符。

		<category>
			<pattern>ONE TIME I *</pattern>
			<template>
				<random>
					<li>Go on.</li>
					<li>How old are you?</li>
					<li>Be more specific.</li>
					<li>I did not know that.</li>
					<li>Are you telling the truth?</li>
					<li>I don't know what that means.</li>
					<li>Try to tell me that another way.</li>
					<li>Are you talking about an animal, vegetable or mineral?</li>
					<li>What is it?</li>
				</random>
			</template>
		</category>
		
# 使用已存在的AIML文件
编写你自己的AIML文件是一个很有趣的事，但是它将花费很大的功夫。我觉得它需要大概10,000个模式才会开始变得真实起来。幸运的是，ALICE基金会提供了大量免费的AIML文件。在[Alice Bot website](http://www.alicebot.org/aiml/aaa/)上浏览AIML文件。在调用std-65percent.xml（它包含了65%最常用的短语）前，有一个浮动值。还有一个文件允许你和机器人玩BlackJack游戏。

# 进入Python
到目前为止，所有都是关于AIML XML文件的。它们每一个都很重要，并将组成机器人的大脑，但是它目前仅是信息。机器人需要活过来。你可以使用任何语言来实现AIML详细说明，但是，一些好人已经用Python实现了。

首先，使用**pip**安装aiml包

		pip install aiml
		
注意，aiml只能在Python 2下工作。[Py3kAiml on GitHub](https://github.com/huntersan9/Py3kAiml)是一个可供选择的Python 3版本。

# 最简单的Python程序
这是我们可以开始的最简单的程序。它创建了一个aiml对象，学习启动文件，然后加载剩余的aiml文件。然后，它已经准备好聊天了，而我们进入了一个不断提示用户消息的无限循环。你将需要输入一个机器人认识的模式。这个模式取决于你加载了哪些AIML文件。

我们将启动文件作为一个单独的实体创建，这样，我们之后可以向机器人添加更多的aiml文件，而不需要修改任何程序源码。我们可以在启动xml文件中添加更多的可供学习的文件。

		import aiml

		# 创建核心，并学习AIML文件
		kernel = aiml.Kernel()
		kernel.learn("std-startup.xml")
		kernel.respond("load aiml b")

		# 按住CTRL-C来终止这个循环
		while True:
			print kernel.respond(raw_input("Enter your message >> "))
			
# 加速Brain加载
当你开始拥有很多AIML文件时，它将花费很长的时间来学习。这就是brain文件从何而来。在机器人学习所有的AIML文件后，它可以直接将它的大脑保存到一个文件中，这个文件将会在后续的运行中动态加速加载时间。

		import aiml
		import os

		kernel = aiml.Kernel()

		if os.path.isfile("bot_brain.brn"):
			kernel.bootstrap(brainFile = "bot_brain.brn")
		else:
			kernel.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
			kernel.saveBrain("bot_brain.brn")

		# kernel now ready for use
		while True:
			print kernel.respond(raw_input("Enter your message >> "))
			
# 在运行的时候重新加载AIML
你可以在机器人运行的时候发送加载消息，然后它将加载AIML文件。记住，如果你使用了上面写的brain方法，在运行的时候加载并不会将新增改变保存到brain中。你将需要删除brain文件以便于它在下一次启动的时候重建，或者需要修改代码，使得它在重新加载后的某个时间点保存brain。关于为机器人创建可以执行的Python命令，查看下一章节。

	load aiml b
	
#增加Python命令
如果你想要为你的机器人提供一些特殊的运行Python函数的命令，那么，你应该为机器人捕获输入消息，然后在将它发送给**kernel.respond()**之前处理它。在上面的例子中，我们从**raw_input**中获得了用户的输入。然而，我们可以从任何地方获取输入。可能是一个TCP socket，或者是一个语音识别源码。在它进入到AIML之前处理这个消息。你可能想要在某些特定的消息上跳过AIML处理。

		while True:
			message = raw_input("Enter your message to the bot: ")
			if message == "quit":
				exit()
			elif message == "save":
				kernel.saveBrain("bot_brain.brn")
			else:
				bot_response = kernel.respond(message)
				# Do something with bot_response

# 会话和断言
通过指定一个会话，AIML可以为不同的人剪裁不同的会话。例如，如果某个人告诉机器人，他的名字是Alice，而另一个人告诉机器人他的名字是Bob，机器人可以区分不同的人。为了指定你所使用的会话，将其作为第二个参数传给**respond()**

		sessionId = 12345
		kernel.respond(raw_input(">>>"), sessionId)
		
这对于为每一个客户端定制个性化的对话是很有帮助的。你将必须以某种形式生成自己的会话ID，并且跟踪它。注意，保存brain文件不会保存所有的会话值。

		sessionId = 12345

		# 会话信息作为字典获取. 包含输入输出历史，
		# 以及任何已知断言
		sessionData = kernel.getSessionData(sessionId)

		# 每一个会话ID需要时一个唯一值。
		# 断言名是机器人在与你的会话中了解到的某些/某个名字 
		# 机器人可能知道，你是"Billy"，而你的狗的名字是"Brandy"
		kernel.setPredicate("dog", "Brandy", sessionId)
		clients_dogs_name = kernel.getPredicate("dog", sessionId)

		kernel.setBotPredicate("hometown", "127.0.0.1")
		bot_hometown = kernel.getBotPredicate("hometown")
		
在AIML中，我们可以使用模板中的**set**响应来设置断言

		<aiml version="1.0.1" encoding="UTF-8">
		   <category>
			  <pattern>MY DOGS NAME IS *</pattern>
			  <template>
				 That is interesting that you have a dog named <set name="dog"><star/></set>
			  </template>  
		   </category>  
		   <category>
			  <pattern>WHAT IS MY DOGS NAME</pattern>
			  <template>
				 Your dog's name is <get name="dog"/>.
			  </template>  
		   </category>  
		</aiml>
		
使用上面的AIML，你可以告诉机器人：

		My dogs name is Max
		
而机器人会回答你：

		That is interesting that you have a dog named Max
		
然后，如果你问机器人：

		What is my dogs name?
		
机器人将会回答：

		Your dog's name is Max.
		
		















