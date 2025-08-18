import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  vus: 500,
  duration: '300s',
};

export default function () {
  let body = JSON.stringify({
    conversation: 'chào bạn',
    keycloakId: '3c3ae1c6-7c92-41f2-a269-38bf8e8e2fdf'
  });

 const jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJGeldUN3dja0U5dzVraWRmV180Q0ZLRnB4NlFEV2dkdS1uY0hvcUNRZTBVIn0.eyJleHAiOjE3NTU0MDI0ODgsImlhdCI6MTc1NTM2NjQ4OCwianRpIjoib25ydHJvOjk4YWU2YjI0LThjNGYtYWJlNC1iYWQ3LTkxODJkMGMyZmYwMSIsImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODA4MS9yZWFsbXMvVXNlclNjaGVkdWxlIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6IjNjM2FlMWM2LTdjOTItNDFmMi1hMjY5LTM4YmY4ZThlMmZkZiIsInR5cCI6IkJlYXJlciIsImF6cCI6InVzZXJfc2NoZWR1bGUiLCJzaWQiOiI4MWQ3MWM2OC01M2RiLTQxZWYtOTBhYy1jMmNiOGY0MWQ0YzMiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwiTUFOQUdFUiIsInVtYV9hdXRob3JpemF0aW9uIiwiQURNSU4iLCJVU0VSIiwiZGVmYXVsdC1yb2xlcy11c2Vyc2NoZWR1bGUiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBlbWFpbCBwcm9maWxlIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJuYW1lIjoiYWRtaW4gYWRtaW4iLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhZG1pbjEiLCJnaXZlbl9uYW1lIjoiYWRtaW4iLCJmYW1pbHlfbmFtZSI6ImFkbWluIiwiZW1haWwiOiJhYmNAZ21haWwuY29tIn0.OhctErfc9F-JuDuinjHf8x0Ppvvx6jnZetZm9lRtp5Y4gBnZzLlfRXCluFaX2vUyAau8todThvbs-ti7r-mhhF9oKtp6xMzTMk18UxA3-AYuTZqhZoTW41Y1FMIgYcPIVKcWIZrPjVCExx2MIXj1-V5rriMZi_SMQgvtt11e7b2IG_o6WLTvSV4E46hwaPNstekKT3PapODrod80UDJTlq-Lm-XcywTErZXxYtXRMTd6t6owGGd1RNBuFHQUzzWiDLW4o7gQKcF-GO73UteYStekHh8ayKlnxYdcF-I1NGBoeXEz7G35lUJ0qPi4l4wlS56x1MMfCK8ERvpTk6QzCw';

  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${jwt}`   // set JWT vào header
  };


  let res = http.post('http://host.docker.internal:5000/api/users/chat', body, { headers });

  console.log("Status:", res.status, "Body:", res.body);

  sleep(1);
}
