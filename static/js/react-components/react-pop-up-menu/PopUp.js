import React from 'react'
import RenderDom from 'react-dom'


export default class PopUp extends React.Component {
  constructor(props){
    super(props)

    this.state = {
      articles : {},
    }
  }

  componentDidMount(){
    this._isMounted = true
  }
  componentWillMount(){

      this.fetchArticles(this.props.item.url, this.props.item.keyword)
  }

  componentWillUnmount(){
    this._isMounted = false
  }

  fetchArticles = async (url, keyword) => {
    try{
      const response = await fetch(`/${url}`, {
        method: 'POST',
        headers: {'content-type': 'application/json'},
        body: JSON.stringify({keyword}),
      })
      const article = await response.json()
      if(this.props.visibility && this._isMounted){
        this.setState({
          articles : article,
        })
      }
    }catch(err){
      if(this.props.visibility && this._isMounted){
        this.setState({
          error: err,
        })
      }
    }
  }

   render(){

      console.log("hallo")
      return(
        <div  className="popup"
              onMouseEnter={this.props.enter}
              onMouseLeave={this.props.leave}
        >
        {this.state.articles.length > 1 &&
          this.state.articles.map((article, index) => {
                if(index === 0){
                  return(
                    <FeaturedArticle
                      key={article.title}
                      title={article.title}
                      body={article.body}
                      imgurl={article.img}
                      slug={article.slug}
                    />
                  )
                }else{
                  return(
                    <Article
                      key={article.title}
                      title={article.title}
                      body={article.body}
                      imgurl={article.img}
                      slug={article.slug}
                    />
                  )
                }
            })

        }
      </div>
      )
    }
}

function deleteMarkup(content){
  var temp = document.createElement('DIV')
  temp.innerHTML = content
  return temp.textContent + "..." || temp.innerText + "..."
  //content.replace(/<.*>/, '').replace(/<.*>/, '')
}
const FeaturedArticle = (props) => {
  return(
    <div className="featured-nav-article">
      <h2>Latest:</h2>
        <a href={"/article/" + props.slug}>
          <img className="react-popup-thumbnail" src={"/static/img/" + props.imgurl} alt={props.title} />
          <h2 className="content">{props.title}</h2>
          <p className="content" >{deleteMarkup(props.body)}</p>
        </a>
    </div>
  )
}
const Article = (props) => {

  return(
    <div className="nav-article">
      <a href={"/article/" + props.slug}>
        <img className="react-popup-thumbnail" src={"/static/img/" + props.imgurl} alt={props.title} />
        <h2 className="content">{props.title}</h2>
        <p className="content">{deleteMarkup(props.body)}</p>
      </a>
    </div>
  )
}
