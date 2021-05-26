// Function module to send asynchronous ajax request

import axios from 'axios'
export default function ajax(url, data={}, type='GET') {
    if(type==='GET') {
        return axios.get(url, {
            params: data
        }).catch( e => {
        if (e.response) {
          console.info(e.response.data)
          console.info(e.response.status)
          console.info(e.response.headers)
        } else if (e.request) {
          console.info(e.request)
        } else {
          console.info('error', e.message)
        }
    console.info(e.config)
      })
    } else {
        return axios.post(url, data)
    }
}