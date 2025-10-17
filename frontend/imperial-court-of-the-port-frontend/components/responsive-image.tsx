import Image from 'next/image';

const ResponsiveImage = ({path}:{path:string}) => {
  return (
    // Set 'position: relative' and define height/width on the parent container
    <div style={{ position: 'relative', width: '100%', height: '400px' }}> 
      <Image
        src={path}
        alt="Eureka landing page image"
        fill // Makes the image fill the parent element
        style={{ objectFit: 'cover' }} // CSS property to crop/fit the image
      />
    </div>
  );
};

export default ResponsiveImage