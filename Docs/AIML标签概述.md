参考[Artificial Intelligence Markup Language (AIML) Version 1.0.1](http://www.alicebot.org/TR/2011/)

# AIML对象结构
## AIML命名空间
略

## AIML元素

		<aiml:aiml version = number>

		   <!-Content: top-level-elements) -->

		</aiml:aiml>
		
一个AIML对象是由一个XML文件中的一个aiml:aiml元素表示的。

一个AIML对象必须有一个version属性，以表示该对象需要的AIML版本。

aiml:aiml元素可能包含了以下的元素：

* aiml:topic
* aiml:category

顶层元素：作为aiml:aiml元素的孩子的元素。

下面是一个AIML对象的顶层结构样例。“...”表示属性值或内容被省略了。AIML对象可能包含了零或多个以下的元素。

		<aiml:aiml  version="1.0.1"
					xmlns:aiml="http://alicebot.org/2001/AIML">

		   <aiml:topic name="...">

			  ...

		   </aiml:topic>

		   <aiml:category>

				 ...

		   </aiml:category>

		</aiml:aiml>
		
也就是说，AIML对象必须包括零个或多个topic元素，和一个或多个categroy元素。

不限制aiml:aiml元素的孩子出现的顺序。

## 向前兼容

一个元素自身向前兼容。

在向前兼容模式下，一个元素：

* 若它是一个顶层元素，而AIML 1.0.1不允许这样的元素作为顶层元素，则这个元素会与它的内容一起被忽略。
* 如果这个元素在category中，而AIML 1.0.1不允许这样的元素出现在category中，这个元素则应该被忽略。
* 如果这个元素有一个AIML 1.0.1不允许出现的属性，或者这个元素有一个AIML 1.0.1不允许出现的可选属性值，那么这个属性则被忽略。

因此，任何AIML 1.0.1解释器必须能够处理以下的AIML对象而不报错：

	<aiml:aiml  version="1.1"
				xmlns:aiml="http://alicebot.org/2001/AIML">

	   <aiml:topic name="demonstration *">

		  <aiml:category>

			 <aiml:pattern>* EXAMPLE</aiml:pattern>

			 <aiml:template>

				This is just an example, <get name="username"/>.

				<aiml:exciting-new-1.1-feature/>

			 </aiml:template>

		  </aiml:category>

	   </aiml:topic>
	   
## AIML模式表达式
有两种：简单的模式表达式，混合模式表达式

## AIML断言处理

许多AIML元素属性处理断言。

---
# Topic

一个topic是一个可选的顶层元素，它包含了category元素。一个topic元素有一个必选的name属性，这个属性必须包含一个简单的模式表达式。一个topic元素可能包含了一个或多个category元素。

topic元素的name属性内容会被附加在一个完整匹配路径上，这个路径是在加载时间由AIML解释器构造的。

		<!-- Category: top-level-element -->

		<aiml:topic
		   name = aiml-simple-pattern-expression >

		   <!-- Content: aiml:category+ -->

		</aiml:topic>
		
# Category

一个category是一个顶层（或者是二层，当它被包含在一个topic中的时候）元素，这个元素正确的包含了一个pattern及一个template。一个category不包含任何属性。

AIML解释器会假设所有不作为一个显式的topic元素的孩子出现的category元素为一个隐式的topic（这个topic的name属性值是*）的孩子。

		<!-- Category: top-level-element -->

		<aiml:category>

		   <!-- Content: aiml-category-elements -->

		</aiml:category>

# Pattern
pattern是一个内容为混合模式表达式的元素。一个category中有且仅有一个pattern。而且,pattern必须为category中的第一个子元素。一个pattern不需要任何属性。

pattern的内容会被附加到在加载时间由AIML解释器构建的完整匹配路径中。

		<!-- Category: aiml-category-elements -->

		<aiml:pattern>

		   <!-- Content: aiml-pattern-expression -->

		</aiml:pattern>
		
## Pattern-side That
pattern-side that 是一个用于上下文匹配的特殊的pattern元素类型。pattern-side在category中是可选的，但如果它出现了，它必须仅出现一次，而且必须紧跟着pattern，并且立即处理template。一个pattern-side that元素包含了一个简单模式表达式

pattern-side that的内容会被附加到在加载时间由AIML解释器构建的完整匹配路径中。

如果一个category不包含一个pattern-side that，AIML解释器必须假设一个隐式的包含了模式表达式*的pattern-side that。

一个pattern-side that元素不包含任何属性。

	<!-- Category: aiml-category-elements -->

	<aiml:that>

	   <!-- Content: aiml-pattern-expression -->

	</aiml:that>
	
# Template

一个template是一个出现在category元素中的元素。它位于pattern-side that元素（若存在）之后，否则位于pattern元素后。一个template元素不包含任何属性。

	<!-- Category: aiml-category-elements -->

	<aiml:template>

	   <!-- Content: aiml-template-elements -->

	</aiml:template>
	
AIML大部分内容是在template中的。template可能包含零到多个混合了字符数据的AIML template元素。

## 原子template元素
AIML中的一个原子template元素暗示AIML解释器必须根据元素的功能性意义返回一个值。原子元素不包含任何内容。

### Star

star元素表示，一个AIML解释器应该在返回template的时候

### Template-side that

### Input

input元素告诉AIML解释器，它应该用前面用户的输入代替内容。

template-side input元素有一个可选的index属性，这个属性可能包含一个单独的整型或者一个由逗号分隔的整形对。index中最小的整型是1.index告诉AIML解释器应该返回前面哪一个用户的输入（第一维度），及可选地前面哪一个用户输入的“句子”。

若在运行期间，指定的index维度都是无效的，AIML解释器应该抛出一个错误。

一个未指明的index是“1,1”的等价。一个未指明的index第二维度是为第二维度指明“1”的等价。

input元素不包含任何内容
		<!-- Category: aiml-template-elements -->

		<aiml:input
		   index = (single-integer-index | comma-separated-integer-pair) />


<未完，待续……>

## 缩写元素
一些原子AIML元素是其他AIML元素组合的缩写。它们下面一一列举，不做进一步说明。对于下面的每一个缩写元素，读者应该参考每一个元素完整的结构的的描述

### SR
sr元素是下面的缩写：

		<srai><star/></srai>
		
原子sr不包含任何内容		
		<!-- Category: aiml-template-elements -->

		<aiml:sr/>

### Person2
person2元素的原子版本是下面的缩写：
	<person2><star/></person2>

原子person2不包含任何内容
		<!-- Category: aiml-template-elements -->

		<aiml:person2/>
		
### Person
person元素的原子版本是下面的缩写：
	<person><star/></person>
	
原子person不包含任何内容
		<!-- Category: aiml-template-elements -->

		<aiml:person/>
		
### Gender
gender元素的原子版本是下面的缩写：
	<gender><star/></gender>
	
原子gender不包含任何内容
		<!-- Category: aiml-template-elements -->

		<aiml:gender/>

## 符号减少元素
AIML定义了一个符号减少元素，叫做srai，和sr这个缩写元素相同。

### SRAI
srai元素命令AIML解释器将srai元素内容的处理结果传给AIML匹配循环，就如由用户的输入一样（包括了逐句通过整个输入标准化过程）。srai元素不包含任何属性。它可能包含任意的AIML template元素。

正如所有的AIML元素，嵌套的表单由里向外解析，因此，嵌入的srai是完美可接受的。

	<!-- Category: aiml-template-elements -->

	<aiml:srai>

	   <!-- Contents: aiml-template-elements -->

	</aiml:srai>


## 转换元素
AIML定义了两种“转换”元素来命令AIML解释去处理它们的内容而不返回任何值。

### Think
think元素命令AIML解释器执行它所有内容的过程，但是不返回任何值，并忽略内容所产生的输出。

think元素没有属性，它可能包含任何AIML template元素。

	<!-- Category: aiml-template-elements -->

	<aiml:think>

	   <!-- Contents: aiml-template-elements -->

	</aiml:think>
	
### Learn
learn元素命令AIML解释器检索由URI指定的资源，丙炔处理它的AIML对象的内容。

	<!-- Category: aiml-template-elements -->

	<aiml:learn>

	   <!-- Contents: uri-reference -->

	</aiml:learn>
