import React from 'react'
import RenderDom from 'react-dom'





const Articles = (props) => {
  props.articles.map(article => (
    <div>
      <h1>{article.title}</h1>
      <p>{article.body}</p>
    </div>
  ))
}

export default class RelatedArticles extends React.Component{
  state = {
    articles = '',
  }

  ComponentDidMount(){
    this._isMounted = true
  }

  
  ComponentWillUnmount(){
    this._isMounted = false
  }


  ComponentWillMount(){
    fetcharticles()
  }

  fetcharticles = async ([keywords]) => {
    try{
      const response = await fetch(`/${url}`, {
        method: 'POST',
        headers: {'content-type': 'text'},
        body: [...keywords],
      })
      const articles = await response.json()
      if(this._isMounted){
        this.setState({
          articles : articles,
        })
      }
    }catch(err){
      if(this._isMounted){
        this.setState({
          error: err,
        })
      }
    }
  }
  render(){

    {if (this.state.articles){
    return(
      <div>
        <Articles articles={this.state.articles} />
      </div>
    )
  }else{
    return null
  }}
  }
}
