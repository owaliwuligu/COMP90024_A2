import React from 'react';
import { connect } from 'dva';
import DataList from '../../components/echart.js';

function IndexPage() {
  return (
      // eslint-disable-next-line no-undef
    <div className={styles.normal}>
       <DataList data={{
        xdata: ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'],
        ydata: {
          ydata1:[2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3],
          ydata2:[2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3],
        }
      }}/>
    </div>
  );
}

IndexPage.propTypes = {
};

export default connect()(IndexPage);
