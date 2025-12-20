import React, { JSX } from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <div className="hero-background-animation"></div>
        <h1 className={clsx('hero__title', styles.heroTitle)}>
          Building the Body for the Artificial Mind.
        </h1>
        <p className={clsx('hero__subtitle', styles.heroSubtitle)}>{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className={clsx('button button--primary button--lg', styles.ctaButton, styles.ctaButtonPrimary)}
            to="/docs/intro-to-ros2/what-is-ros2">
            Start Learning
          </Link>
          <Link
            className={clsx('button button--secondary button--lg', styles.ctaButton, styles.ctaButtonSecondary)}
            href="https://github.com/Muhammad-Saad-Ahmed/Hackathon-1_Physical-AI_Humanoid_Book">
            View GitHub
          </Link>
        </div>
      </div>
    </header>
  );
}

const FeatureList = [
  {
    title: 'ROS 2 Native',
    Svg: () => (
      <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 2L2 7V17L12 22L22 17V7L12 2Z" stroke="#00f0ff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        <path d="M2 7L12 12L22 7" stroke="#00f0ff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        <path d="M12 12V22" stroke="#00f0ff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      </svg>
    ),
    description: (
      <>
        Leverage the full power of the Robot Operating System (ROS 2), the industry-standard framework for robotics middleware.
      </>
    ),
  },
  {
    title: 'Sim-First Approach',
    Svg: () => (
       <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
         <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" stroke="#00f0ff" strokeWidth="2" strokeLinejoin="round"/>
         <path d="M3.27 6.96L12 12.01l8.73-5.05" stroke="#00f0ff" strokeWidth="2" strokeLinejoin="round"/>
         <path d="M12 22.08V12" stroke="#00f0ff" strokeWidth="2" strokeLinejoin="round"/>
      </svg>
    ),
    description: (
      <>
        Design, test, and iterate in high-fidelity simulators like Gazebo and Isaac Sim before deploying to physical hardware.
      </>
    ),
  },
  {
    title: 'VLA Ready',
    Svg: () => (
      <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M15 10L20.5 10" stroke="#00f0ff" strokeWidth="2" strokeLinecap="round"/>
        <path d="M17.5 12.5L17.5 7.5" stroke="#00f0ff" strokeWidth="2" strokeLinecap="round"/>
        <path d="M3 13L9 13" stroke="#00f0ff" strokeWidth="2" strokeLinecap="round"/>
        <path d="M6 15.5L6 10.5" stroke="#00f0ff" strokeWidth="2" strokeLinecap="round"/>
        <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="#00f0ff" strokeWidth="2"/>
      </svg>
    ),
    description: (
      <>
        Integrate cutting-edge Vision-Language-Action models to give your humanoids unprecedented understanding and interaction capabilities.
      </>
    ),
  },
];

function Feature({title, Svg, description}) {
  return (
    <div className={clsx('col col--4', styles.feature)}>
      <div className="text--center">
        <Svg alt={title} />
      </div>
      <div className="text--center padding-horiz--md">
        <h3 className={styles.featureTitle}>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}


export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Home`}
      description="A guide to building the next generation of intelligent humanoid robots with modern AI.">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              {FeatureList.map((props, idx) => (
                <Feature key={idx} {...props} />
              ))}
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}