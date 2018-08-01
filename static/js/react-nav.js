


const styles ={
}



class MenuItem extends React.Component {
  constructor(props){
    super(props)

    this.state = {
      showMenu : false,
    }
  }

  componentWillUnmount(){
    clearTimeout(this.wait)
  }
  handleMouseOver = () => {
    if(this.wait){
      clearTimeout(this.wait)
    }
    this.setState({
      showMenu: true,
      })

  }

  handleMouseOut = () => {
      this.wait = setTimeout(() => {
        this.setState({
          showMenu: false,
      })
    },100)
  }

  render(){

    return(
        <a className="react-menu-item-link" href={this.props.item.link}>
          <div
            className="react-menu-item dropdown-item"
            onMouseEnter={this.handleMouseOver}
            onMouseLeave={this.handleMouseOut}
          >
            <i className="fa fa-plus"></i>
              {this.props.name}
            {this.state.showMenu &&
              <PopUp
                visibility={this.state.showMenu}
                enter={this.handleMouseOver}
                leave={this.handleMouseOut}
                name={this.props.name}
                item={this.props.item}
              />
            }
          </div>
        </a>
    )
  }
}

class PopUp extends React.Component {
  constructor(props){
    super(props)

    this.state = {
      articles : {},
    }
  }

  componentDidMount(){
  }
  componentWillMount(){

      this.fetchArticles(this.props.item.url, this.props.item.keyword)
  }

  componentWillUnmount(){
  }

  fetchArticles = async (url, keyword) => {
    try{
      const response = await fetch(`/${url}`, {
        method: 'POST',
        headers: {'content-type': 'application/json'},
        body: JSON.stringify({keyword}),
      })
      const article = await response.json()
      if(this.props.visibility){
        this.setState({
          articles : article,
        })
      }
    }catch(err){
      this.setState({
        error: err,
      })
    }
  }

   render(){


      return(
        <div  className="popup"
              onMouseEnter={this.props.enter}
              onMouseLeave={this.props.leave}
        >
        {this.state.articles.length > 0 &&
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
      <img className="react-popup-thumbnail" src={"/static/img/" + props.imgurl} alt={props.title} />
      <h2 className="content">{props.title}</h2>
      <p className="content" >{deleteMarkup(props.body)}</p>
    </div>
  )
}
const Article = (props) => {

  return(
    <div className="nav-article">
      <img className="react-popup-thumbnail" src={"/static/img/" + props.imgurl} alt={props.title} />
      <h2 className="content">{props.title}</h2>
      <p className="content">{deleteMarkup(props.body)}</p>
    </div>
  )
}

class DropdownList extends React.Component {


  render(){

      this.menuitems = this.props.items.map(item => {
        return(
            <MenuItem
                key={item.name}
                name={item.name}
                item={item}
            />
        )
      })

    return (
              <div>
                {this.menuitems}
              </div>
      )
  }
}

const MENUITEMS = [
  {
    name : 'Recent',
    link: '/blog',
    url : 'fetcharticles',
    keyword: 'Recent',
  },
  {
    name : 'Travel',
    link: '/blog/travel',
    url : 'fetcharticles',
    keyword: 'Travel',
  },
  {
    name : 'Work',
    link: '/blog/work',
    url : 'fetcharticles',
    keyword: 'Work',
  },
  {
    name : 'Photography',
    link: '/blog/photography',
    url : 'fetcharticles',
    keyword: 'Photography',
  },
]


ReactDOM.render(
  <DropdownList items={MENUITEMS} />,
  document.getElementById('react-menu-item')
);
