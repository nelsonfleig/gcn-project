import React, {Component} from 'react';
import { useParams } from 'react-router-dom';
import Flask from '../util/Flask';

class ArtistPage extends Component {
    
    constructor(props) {
        super(props)

        this.state = {
            artist: null
        }

    }

    componentDidMount() {
        //this.loadArtistInfo();
        let {mbid} = useParams();
        Flask.getArtistById(mbid).then(artist => {
            this.setState({
                artist: artist
            })
        })
    }

    loadArtistInfo() {
        //const mbid = "f8365a1d-6b16-43fc-a8b6-3de0f64a0409"
        // let {mbid} = useParams();
        // Flask.getArtistById(mbid).then(artist => {
        //     this.setState({
        //         artist: artist
        //     })
        // })
        
    }


    render() {
        
        // const predictions = this.state.artist.predictions.map(prediction => {
        //     return (<p>{prediction}</p>)
        // })


        //console.log(this.state.artist)

        if (this.state.artist != null) {
            return (<div>{this.state.artist.name}</div>)
        } else {
            return <div>No artist</div>
        }
    }
}
        
        



export default ArtistPage;