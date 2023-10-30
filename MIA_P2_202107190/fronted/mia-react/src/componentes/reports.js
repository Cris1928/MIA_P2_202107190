import React, { useEffect, useState } from 'react';
import mbr from "../reportes/mbr.png"
import bm_inode from "../reportes/bm_inode.png"
import reporte_journaling from "../reportes/reporte_journaling.png"
import reporte_tree from "../reportes/reporte_tree.png"
import bm_block from "../reportes/bm_block.png"
import disk from "../reportes/disk.png"
import reporte_inodos from "../reportes/reporte_inodos.png"
import reporte_superbloque from "../reportes/reporte_superbloque.png"
function Reports_Card() {
    const blobToBase64 = (blob) => {
        return new Promise( (resolve, reject) =>{
            const reader = new FileReader();
            reader.readAsDataURL(blob);
            reader.onloadend = () => {
                resolve(reader.result.split(',')[1]);
                // "data:image/jpg;base64,    =sdCXDSAsadsadsa"
            };
        });
    };
    const [base64Image, setBase64Image] = useState('');
    const [base64Image2, setBase64Image2] = useState('');
    const [base64Image3, setBase64Image3] = useState('');
    const [base64Image4, setBase64Image4] = useState('');
    const [base64Image5, setBase64Image5] = useState('');
    const [base64Image6, setBase64Image6] = useState('');
    const [base64Image7, setBase64Image7] = useState('');
    const [base64Image8, setBase64Image8] = useState('');

    useEffect(() => {
      const imagePath = mbr;
      const imagePath2 = bm_inode;
      const imagePath3 = reporte_journaling;
      const imagePath4 = reporte_tree;
      const imagePath5 = bm_block;
      const imagePath6 = disk;
      const imagePath7 = reporte_inodos;
      const imagePath8 = reporte_superbloque;
  
      const loadImageAsBase64 = async () => {
        try {
          const response = await fetch(imagePath);
          const blob = await response.blob();

          const response2 = await fetch(imagePath2);
          const blob2 = await response2.blob();
  

          const response3 = await fetch(imagePath3);
          const blob3 = await response3.blob();


          const response4 = await fetch(imagePath4);
          const blob4 = await response4.blob();

          const response5 = await fetch(imagePath5);
          const blob5 = await response5.blob();

          const response6 = await fetch(imagePath6);
          const blob6 = await response6.blob();

          const response7 = await fetch(imagePath7);
          const blob7 = await response7.blob();


          const response8 = await fetch(imagePath8);
          const blob8 = await response8.blob();


          const reader = new FileReader();
          reader.onloadend = () => {
         
            setBase64Image(reader.result);
            console.log(reader.result)
          };

          const reader2 = new FileReader();
          reader2.onloadend = () => {
         
            setBase64Image2(reader2.result);
            console.log(reader2.result)
          };        


          const reader3 = new FileReader();
          reader3.onloadend = () => {
         
            setBase64Image3(reader3.result);
            console.log(reader3.result)
          };        

          const reader4 = new FileReader();
          reader4.onloadend = () => {
         
            setBase64Image4(reader4.result);
            console.log(reader4.result)
          };        



          const reader5 = new FileReader();
          reader5.onloadend = () => {
         
            setBase64Image5(reader5.result);
            console.log(reader5.result)
          }; 


          const reader6 = new FileReader();
          reader6.onloadend = () => {
         
            setBase64Image6(reader6.result);
            console.log(reader6.result)
          }; 


          const reader7 = new FileReader();
          reader7.onloadend = () => {
         
            setBase64Image7(reader7.result);
            console.log(reader7.result)
          }; 

          const reader8 = new FileReader();
          reader8.onloadend = () => {
         
            setBase64Image8(reader8.result);
            console.log(reader8.result)
          }; 

          reader.readAsDataURL(blob);
          reader2.readAsDataURL(blob2);
          reader3.readAsDataURL(blob3);
          reader4.readAsDataURL(blob4);
          reader5.readAsDataURL(blob5);
          reader6.readAsDataURL(blob6);
          reader7.readAsDataURL(blob7);
          reader8.readAsDataURL(blob8);
        } catch (error) {
          console.error('Error al cargar la imagen:', error);
        }
      };



      loadImageAsBase64();
  }, []);
  return (
    <div className="Reports_Card">
    <h1>reporte mbr</h1>
    
    <img src= {base64Image}/>
    <h1>reporte bm_inode</h1>
    <img src= {base64Image2}/>
    <h1>reporte_journaling</h1>
    <img src= {base64Image3}/>
    <h1>reporte_tree</h1>
    <img src= {base64Image4}/>
    <h1>bm_block</h1>
    <img src= {base64Image5}/>
    <h1>disk</h1>
    <img src= {base64Image6}/>
    <h1>reporte_inodos</h1>
    <img src= {base64Image7}/>
    <h1>reporte_superbloque</h1>
    <img src= {base64Image8}/>
  </div>
  );
}

export default Reports_Card;