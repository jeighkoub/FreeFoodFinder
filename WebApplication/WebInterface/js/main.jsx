import React from 'react';
import ReactDOM from 'react-dom';

class Index extends React.Component {
    // set the default state of the constructor
    constructor(props) {
        super(props);
        this.state = { events: [], filters:{}, };
    }

    componentDidMount() {
        // make a fetch request or something to get the events from the table/web scraper... 
        return; // currently does nothing
      }

      // Main render function
  render() {
    return (
        // make event a component, as well as the filters... 
        // each event could be a Panel - using bootstrap add on I found here https://react-bootstrap-v3.netlify.app/components/panel/ 
      <span>Main Page</span> 
    );
  }
}

export default Index;
ReactDOM.render(<Index />, document.getElementById('reactEntry'));
